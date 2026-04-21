#!/usr/bin/env python3
"""
5-Step Reasoning Pipeline Generator for BiomedSearch.

Steps:
  1. Classify experiment type (BM25 on experiment-types.csv)
  2. Match reasoning rules (analysis-reasoning.csv by category)
  3. Multi-domain parallel search (tools + databases + workflows)
  4. Weighted best-match selection (post-BM25 rerank on bounded set)
  5. Assemble pipeline with Installed/External flags and actionable handoffs
"""

import re
from pathlib import Path
from typing import Optional

from core import BiomedSearch, _load_csv, DATA_DIR


def _parse_list(field: str) -> list:
    return [x.strip() for x in field.split(';') if x.strip()]


def _parse_params(field: str) -> dict:
    params = {}
    for item in field.split(';'):
        item = item.strip()
        if '=' in item:
            k, v = item.split('=', 1)
            params[k.strip()] = v.strip()
    return params


class PipelineGenerator:
    def __init__(self, engine: BiomedSearch):
        self.engine = engine
        self._reasoning_rows = None

    def _get_reasoning(self) -> list:
        if self._reasoning_rows is None:
            self._reasoning_rows = _load_csv(DATA_DIR / 'analysis-reasoning.csv')
        return self._reasoning_rows

    def generate(self, query: str) -> dict:
        experiment = self._classify_experiment(query)
        rules = self._match_rules(experiment)
        resources = self._multi_domain_search(query, rules)
        selected = self._select_best_matches(resources)
        return self._assemble_pipeline(query, experiment, rules, selected)

    def _classify_experiment(self, query: str) -> Optional[dict]:
        results = self.engine.search(query, domain='experiment', max_results=1)
        if results:
            return results[0]
        return None

    def _match_rules(self, experiment: Optional[dict]) -> Optional[dict]:
        if not experiment:
            return None
        category = experiment.get('Category', '')
        if not category:
            return None
        for row in self._get_reasoning():
            if row.get('Experiment_Category', '').lower() == category.lower():
                rule = dict(row)
                rule['_parsed_params'] = _parse_params(row.get('Key_Parameters', ''))
                rule['_parsed_tools'] = _parse_list(row.get('Tool_Priority', ''))
                rule['_parsed_dbs'] = _parse_list(row.get('Database_Priority', ''))
                rule['_parsed_anti'] = _parse_list(row.get('Anti_Patterns', ''))
                return rule
        return None

    def _multi_domain_search(self, query: str, rules: Optional[dict]) -> dict:
        boosted = query
        if rules:
            extras = []
            for tid in rules.get('_parsed_tools', [])[:3]:
                parts = tid.split('-', 1)
                if len(parts) == 2:
                    extras.append(parts[1])
            for did in rules.get('_parsed_dbs', [])[:3]:
                parts = did.split('-', 1)
                if len(parts) == 2:
                    extras.append(parts[1])
            if extras:
                boosted = f'{query} {" ".join(extras)}'

        tools = self.engine.search(boosted, domain='tool', max_results=5)
        databases = self.engine.search(boosted, domain='database', max_results=5)
        workflows = self.engine.search(boosted, domain='workflow', max_results=3)
        return {'tools': tools, 'databases': databases, 'workflows': workflows}

    def _select_best_matches(self, resources: dict) -> dict:
        selected = {}
        for kind, items in resources.items():
            if not items:
                selected[kind] = []
                continue
            reranked = []
            for item in items:
                score = item.get('_score', 0)
                name_fields = ['Tool_Name', 'Database_Name', 'Workflow_Name']
                for nf in name_fields:
                    nv = item.get(nf, '').lower()
                    if nv:
                        score *= 1.0
                        break
                reranked.append(item)
            reranked.sort(key=lambda x: x.get('_score', 0), reverse=True)
            seen = set()
            deduped = []
            for r in reranked:
                cid = r.get('canonical_id', '')
                if cid and cid in seen:
                    continue
                if cid:
                    seen.add(cid)
                deduped.append(r)
            selected[kind] = deduped
        return selected

    def _assemble_pipeline(self, query: str, experiment: Optional[dict],
                           rules: Optional[dict], selected: dict) -> dict:
        pipeline = {
            'query': query,
            'experiment': experiment,
            'reasoning': None,
            'tools': [],
            'databases': [],
            'workflows': [],
        }
        if rules:
            pipeline['reasoning'] = {
                'category': rules.get('Experiment_Category', ''),
                'severity': rules.get('Severity', ''),
                'recommended_pipeline': rules.get('Recommended_Pipeline', ''),
                'decision_rules': rules.get('Decision_Rules', ''),
                'anti_patterns': rules.get('_parsed_anti', []),
                'key_parameters': rules.get('_parsed_params', {}),
                'tool_priority': rules.get('_parsed_tools', []),
                'database_priority': rules.get('_parsed_dbs', []),
            }
        for kind in ['tools', 'databases', 'workflows']:
            pipeline[kind] = []
            for item in selected.get(kind, []):
                entry = {
                    'name': (item.get('Tool_Name') or item.get('Database_Name')
                             or item.get('Workflow_Name') or '?'),
                    'canonical_id': item.get('canonical_id', ''),
                    'score': item.get('_score', 0),
                    'installed': item.get('Installed', 'unknown'),
                    'best_for': item.get('Best_For', ''),
                }
                skill = item.get('Skill_Name', '')
                if skill:
                    entry['skill_name'] = skill
                    entry['skill_dir'] = str(Path.home() / '.claude' / 'skills' / skill)
                    entry['next_action'] = f'Invoke skill: {skill}'
                if kind == 'tools':
                    entry['category'] = item.get('Category', '')
                    entry['example_workflow'] = item.get('Example_Workflow', '')
                elif kind == 'databases':
                    entry['api_type'] = item.get('API_Type', '')
                    entry['data_type'] = item.get('Data_Type', '')
                elif kind == 'workflows':
                    entry['steps'] = item.get('Steps', '')
                    entry['estimated_time'] = item.get('Estimated_Time', '')
                pipeline[kind].append(entry)
        return pipeline

    def format_ascii(self, pipeline: dict) -> str:
        lines = [f'=== Analysis Pipeline: {pipeline["query"]} ===', '']

        exp = pipeline.get('experiment')
        if exp:
            name = exp.get('Experiment_Type', '?')
            cat = exp.get('Category', '')
            lines.append(f'Experiment: {name} ({cat})')
            wf = exp.get('Typical_Workflow', '')
            if wf:
                lines.append(f'Typical Workflow: {wf}')
            lines.append('')

        rules = pipeline.get('reasoning')
        if rules:
            lines.append(f'--- Reasoning ({rules.get("severity", "")}) ---')
            lines.append(f'Category: {rules.get("category", "")}')
            lines.append(f'Recommended: {rules.get("recommended_pipeline", "")}')
            params = rules.get('key_parameters', {})
            if params:
                lines.append('Key Parameters:')
                for k, v in params.items():
                    lines.append(f'  {k} = {v}')
            anti = rules.get('anti_patterns', [])
            if anti:
                lines.append('Anti-Patterns:')
                for a in anti:
                    lines.append(f'  ! {a}')
            decisions = rules.get('decision_rules', '')
            if decisions:
                lines.append(f'Decision Rules: {decisions}')
            lines.append('')

        for kind, label in [('tools', 'Tools'), ('databases', 'Databases'), ('workflows', 'Workflows')]:
            items = pipeline.get(kind, [])
            if not items:
                continue
            lines.append(f'--- {label} ---')
            for i, item in enumerate(items, 1):
                flag = '[INSTALLED]' if item.get('installed') == 'yes' else '[EXTERNAL]'
                lines.append(f'  {i}. {item["name"]} {flag} (score: {item.get("score", 0)})')
                if item.get('best_for'):
                    lines.append(f'     Best for: {item["best_for"]}')
                if item.get('next_action'):
                    lines.append(f'     -> {item["next_action"]}')
                if kind == 'workflows' and item.get('steps'):
                    for step in item['steps'].split(';'):
                        lines.append(f'     {step.strip()}')
            lines.append('')

        return '\n'.join(lines)

    def format_markdown(self, pipeline: dict) -> str:
        lines = [f'# Analysis Pipeline: {pipeline["query"]}', '']

        exp = pipeline.get('experiment')
        if exp:
            lines.append(f'## Experiment Type')
            lines.append(f'**{exp.get("Experiment_Type", "?")}** ({exp.get("Category", "")})')
            wf = exp.get('Typical_Workflow', '')
            if wf:
                lines.append(f'- Typical Workflow: `{wf}`')
            lines.append('')

        rules = pipeline.get('reasoning')
        if rules:
            sev = rules.get('severity', '')
            lines.append(f'## Reasoning Rules (Severity: **{sev}**) ')
            lines.append(f'- **Category:** {rules.get("category", "")}')
            lines.append(f'- **Recommended Pipeline:** `{rules.get("recommended_pipeline", "")}`')
            params = rules.get('key_parameters', {})
            if params:
                lines.append('')
                lines.append('### Key Parameters')
                lines.append('')
                lines.append('| Parameter | Value |')
                lines.append('|-----------|-------|')
                for k, v in params.items():
                    lines.append(f'| {k} | `{v}` |')
            anti = rules.get('anti_patterns', [])
            if anti:
                lines.append('')
                lines.append('### Anti-Patterns')
                for a in anti:
                    lines.append(f'- {a}')
            decisions = rules.get('decision_rules', '')
            if decisions:
                lines.append('')
                lines.append('### Decision Rules')
                lines.append(f'> {decisions}')
            lines.append('')

        for kind, label in [('tools', 'Tools'), ('databases', 'Databases'), ('workflows', 'Workflows')]:
            items = pipeline.get(kind, [])
            if not items:
                continue
            lines.append(f'## {label}')
            lines.append('')
            lines.append('| # | Name | Status | Score | Best For |')
            lines.append('|---|------|--------|-------|----------|')
            for i, item in enumerate(items, 1):
                flag = 'Installed' if item.get('installed') == 'yes' else 'External'
                lines.append(f'| {i} | {item["name"]} | {flag} | {item.get("score", 0)} | {item.get("best_for", "")} |')
            lines.append('')

            installed_items = [item for item in items if item.get('next_action')]
            if installed_items:
                lines.append('### Next Actions')
                for item in installed_items:
                    lines.append(f'- `{item["name"]}`: {item["next_action"]} (`{item.get("skill_dir", "")}`)')
                lines.append('')

            if kind == 'workflows':
                for item in items:
                    steps = item.get('steps', '')
                    if steps:
                        lines.append(f'#### {item["name"]} Steps')
                        for step in steps.split(';'):
                            s = step.strip()
                            if s:
                                lines.append(f'{s}')
                        lines.append('')

        return '\n'.join(lines)
