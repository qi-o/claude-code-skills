#!/usr/bin/env python3
"""
BiomedSearch CLI — Unified discovery/dispatch layer for bioinformatics skills.

Usage:
    python biomed_search.py "差异表达分析"
    python biomed_search.py "单细胞RNA-seq" --domain experiment --format json
    python biomed_search.py "代谢组学" --all
    python biomed_search.py "单细胞RNA-seq差异表达分析" --pipeline
    python biomed_search.py "bulk RNA-seq差异表达" --pipeline --persist my-project
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core import BiomedSearch, AVAILABLE_DOMAINS, CSV_CONFIG

_PIPELINE_HELP = 'Generate a full analysis pipeline with reasoning rules'
_PERSIST_HELP = 'Save pipeline output to analysis-pipeline/<name>/MASTER.md'
_ALL_HELP = 'Search across all domains (database, tool, workflow, experiment)'


def format_ascii(results: list, domain: str) -> str:
    if not results:
        return f'No results found in {domain}.'
    display = CSV_CONFIG[domain]['display_name']
    lines = [f'=== {display} ===', '']
    for i, r in enumerate(results, 1):
        name = r.get('Database_Name') or r.get('Tool_Name') or r.get('Workflow_Name') or r.get('Experiment_Type') or '?'
        score = r.get('_score', 0)
        lines.append(f'[{i}] {name}  (score: {score})')
        installed = r.get('Installed', '')
        if installed:
            flag = 'INSTALLED' if installed == 'yes' else 'EXTERNAL'
            lines.append(f'    Status: {flag}')
        best_for = r.get('Best_For', '')
        if best_for:
            lines.append(f'    Best for: {best_for}')
        skill = r.get('Skill_Name', '')
        if skill:
            lines.append(f'    Skill: {skill}')
        action = r.get('_next_action', '')
        if action:
            lines.append(f'    Action: {action}')
        lines.append('')
    return '\n'.join(lines)


def format_ascii_all(all_results: dict) -> str:
    if not all_results:
        return 'No results found across any domain.'
    parts = []
    for domain, results in all_results.items():
        parts.append(format_ascii(results, domain))
    return '\n'.join(parts)


def format_markdown(results: list, domain: str) -> str:
    if not results:
        return f'**No results found in {domain}.**'
    display = CSV_CONFIG[domain]['display_name']
    lines = [f'## {display}', '']
    for i, r in enumerate(results, 1):
        name = r.get('Database_Name') or r.get('Tool_Name') or r.get('Workflow_Name') or r.get('Experiment_Type') or '?'
        score = r.get('_score', 0)
        installed = r.get('Installed', '')
        badge = ' ![installed](yes)' if installed == 'yes' else (' ![external](ext)' if installed == 'external' else '')
        lines.append(f'### {i}. {name}{badge}  `{score}`')
        best_for = r.get('Best_For', '')
        if best_for:
            lines.append(f'- **Best for:** {best_for}')
        skill = r.get('Skill_Name', '')
        if skill:
            lines.append(f'- **Skill:** `{skill}`')
            lines.append(f'- **Directory:** `{r.get("_skill_dir", "")}`')
        lines.append('')
    return '\n'.join(lines)


def format_markdown_all(all_results: dict) -> str:
    if not all_results:
        return '**No results found.**'
    lines = ['# BiomedSearch Results', '']
    for domain, results in all_results.items():
        lines.append(format_markdown(results, domain))
    return '\n'.join(lines)


def sanitize_name(name: str) -> str:
    return re.sub(r'[^\w\-]', '-', name).strip('-') or 'project'


def main():
    parser = argparse.ArgumentParser(
        description='BiomedSearch — Bioinformatics knowledge discovery engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('query', help='Search query (Chinese or English)')
    parser.add_argument('--domain', '-d', choices=AVAILABLE_DOMAINS,
                        help='Search domain (auto-detected if omitted)')
    parser.add_argument('--all', '-a', dest='search_all', action='store_true',
                        help=_ALL_HELP)
    parser.add_argument('--pipeline', '-p', action='store_true',
                        help=_PIPELINE_HELP)
    parser.add_argument('--max-results', '-n', type=int, default=5,
                        help='Max results per domain (default: 5)')
    parser.add_argument('--format', '-f', choices=['ascii', 'markdown', 'json'],
                        default='ascii', help='Output format (default: ascii)')
    parser.add_argument('--persist', metavar='NAME',
                        help=_PERSIST_HELP)
    args = parser.parse_args()

    engine = BiomedSearch()

    if args.pipeline:
        from pipeline_generator import PipelineGenerator
        gen = PipelineGenerator(engine)
        pipeline = gen.generate(args.query)
        if args.persist:
            slug = sanitize_name(args.persist)
            out_dir = Path('analysis-pipeline') / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            master = out_dir / 'MASTER.md'
            master.write_text(gen.format_markdown(pipeline), encoding='utf-8')
            print(f'Pipeline saved to {master}')
            return
        if args.format == 'json':
            print(json.dumps(pipeline, ensure_ascii=False, indent=2))
        elif args.format == 'markdown':
            print(gen.format_markdown(pipeline))
        else:
            print(gen.format_ascii(pipeline))
        return

    if args.search_all:
        all_results = engine.search_all_domains(args.query, max_results=args.max_results)
        if args.format == 'json':
            print(json.dumps(all_results, ensure_ascii=False, indent=2))
        elif args.format == 'markdown':
            print(format_markdown_all(all_results))
        else:
            print(format_ascii_all(all_results))
        return

    results = engine.search(args.query, domain=args.domain, max_results=args.max_results)
    domain = args.domain or (results[0]['_domain'] if results else 'tool')
    if args.format == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.format == 'markdown':
        print(format_markdown(results, domain))
    else:
        print(format_ascii(results, domain))


if __name__ == '__main__':
    main()
