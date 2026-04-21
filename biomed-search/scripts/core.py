#!/usr/bin/env python3
"""
BM25 Search Engine for Bioinformatics Knowledge Base.
Zero-dependency (stdlib only). Searches CSV knowledge domains.

Usage:
    from core import BiomedSearch
    engine = BiomedSearch()
    results = engine.search("差异表达分析", domain="tool")
"""

import csv
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Optional

# Windows UTF-8 forcing
for _stream in [sys.stdout, sys.stderr]:
    if hasattr(_stream, 'reconfigure'):
        try:
            _stream.reconfigure(encoding='utf-8', errors='backslashreplace')
        except (AttributeError, Exception):
            pass

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'

# Biomedical CJK phrases to preserve as single tokens
_BIOMED_PHRASES = [
    '差异表达', '单细胞', '通路富集', '蛋白质结构', '代谢组学',
    '基因组学', '转录组', '染色质', '免疫沉淀', '靶向药物',
    '基因表达', '变异注释', '临床意义', '致病性', '生物标志物',
    '全基因组', '外显子', '转录组测序', '表观遗传', '信号通路',
    '蛋白互作', '药物发现', '靶点发现', '临床变异', '结构预测',
    '群体频率', '基因组注释', '蛋白质组学', '染色质可及性',
    '基因本体', '单细胞转录组', '药物靶点',
]

# CSV domain configuration
CSV_CONFIG = {
    'database': {
        'file': DATA_DIR / 'databases.csv',
        'search_cols': ['Database_Name', 'Keywords', 'Primary_Use_Case', 'Best_For', 'Example_Queries'],
        'output_cols': ['canonical_id', 'Database_Name', 'API_Type', 'Data_Type', 'Primary_Use_Case', 'Best_For', 'Limitations', 'Skill_Name', 'Installed'],
        'display_name': 'Bioinformatics Databases',
    },
    'tool': {
        'file': DATA_DIR / 'tools.csv',
        'search_cols': ['Tool_Name', 'Keywords', 'Best_For', 'Example_Workflow', 'Category'],
        'output_cols': ['canonical_id', 'Tool_Name', 'Category', 'Input_Type', 'Output_Type', 'Best_For', 'Dependencies', 'Skill_Name', 'Example_Workflow', 'Installed'],
        'display_name': 'Analysis Tools',
    },
    'workflow': {
        'file': DATA_DIR / 'workflows.csv',
        'search_cols': ['Workflow_Name', 'Keywords', 'Best_For', 'Steps'],
        'output_cols': ['canonical_id', 'Workflow_Name', 'Category', 'Steps', 'Required_Tools', 'Required_Databases', 'Best_For', 'Estimated_Time'],
        'display_name': 'Research Workflows',
    },
    'experiment': {
        'file': DATA_DIR / 'experiment-types.csv',
        'search_cols': ['Experiment_Type', 'Keywords', 'Notes', 'Category'],
        'output_cols': ['canonical_id', 'Experiment_Type', 'Category', 'Primary_Tools', 'Required_Databases', 'Typical_Workflow', 'Data_Format', 'Notes'],
        'display_name': 'Experiment Types',
    },
    'reasoning': {
        'file': DATA_DIR / 'analysis-reasoning.csv',
        'search_cols': ['Experiment_Category', 'Recommended_Pipeline', 'Tool_Priority', 'Database_Priority', 'Decision_Rules'],
        'output_cols': ['canonical_id', 'Experiment_Category', 'Recommended_Pipeline', 'Tool_Priority', 'Database_Priority', 'Key_Parameters', 'Anti_Patterns', 'Decision_Rules', 'Severity'],
        'display_name': 'Analysis Reasoning Rules',
    },
}

AVAILABLE_DOMAINS = list(CSV_CONFIG.keys())

# Domain detection keyword sets (substring matching, no \b regex)
DOMAIN_KEYWORDS = {
    'database': {
        'kegg', 'reactome', 'clinvar', 'ensembl', 'opentargets', 'string',
        'uniprot', 'pdb', 'alphafold', 'drugbank', 'hmdb', 'geo', 'ncbi',
        'clinicaltrials', 'pubmed', 'biorxiv', 'semantic scholar', 'scholar',
        '数据库', '通路数据库', '变异数据库', '结构数据库', '药物数据库',
        'metabolite', 'protein database', 'gene database', 'pathway database',
        'gnomad', 'clingen', 'gene ontology',
    },
    'tool': {
        'scanpy', 'pydeseq2', 'deseq2', 'biopython', 'anndata', 'bioservices',
        'matplotlib', 'seaborn', 'bcftools', 'pydicom', 'graphpad', 'blast',
        'samtools', 'fastqc', 'multiqc', 'bedtools', 'star', 'gatk', 'macs2',
        '工具', '分析工具', '可视化', '软件', '分析软件',
    },
    'workflow': {
        'pipeline', '流程', '工作流', '分析流程', '差异表达', '通路富集',
        'variant annotation', '变异注释', '聚类分析', 'target discovery',
        '靶点发现', '蛋白质结构分析', 'drug discovery', '药物发现',
        'complete pipeline', '全流程', '标准流程',
    },
    'experiment': {
        'rna-seq', 'scrna-seq', '单细胞', 'bulk rna', 'wgs', 'wes', 'gwas',
        'proteomics', '蛋白质组', 'metabolomics', '代谢组', 'chip-seq', 'atac-seq',
        '全基因组', '外显子', '转录组', '表观基因组', 'epigenomics',
        '结构预测', '结构生物学', '临床试验', '医学影像',
    },
    'reasoning': {
        'reasoning', '推理', '决策', 'decision', 'rule', '规则',
        'anti-pattern', '反模式', 'best practice', '最佳实践',
        '参数', 'parameter', 'decision rule',
    },
}


class BM25:
    """Okapi BM25 ranking algorithm with mixed CJK/Latin tokenizer."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_freq = Counter()
        self.doc_len = []
        self.corpus = []
        self.avgdl = 0.0
        self.N = 0

    def tokenize(self, text: str) -> list:
        if not text:
            return []
        text = str(text).lower()
        # Preserve known biomedical CJK phrases as single tokens
        for phrase in _BIOMED_PHRASES:
            text = text.replace(phrase, f'\x00{phrase}\x00')
        # Split on preserved-phrase markers, apply CJK splitting only to non-preserved parts
        parts = text.split('\x00')
        tokens = []
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 1:
                # This is a preserved phrase
                tokens.append(part)
            else:
                # Apply CJK char splitting + Latin term extraction to unprotected text
                expanded = re.sub(r'([一-鿿])', r' \1 ', part)
                for t in re.findall(r'[a-z][a-z0-9\-]*|[一-鿿]', expanded):
                    tokens.append(t)
        return tokens

    def fit(self, documents: list):
        self.N = len(documents)
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.doc_len = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_len) / max(self.N, 1)
        self.doc_freq = Counter()
        for tokens in self.corpus:
            for t in set(tokens):
                self.doc_freq[t] += 1

    def score(self, query: str) -> list:
        qtokens = self.tokenize(query)
        scores = []
        for i, doc_tokens in enumerate(self.corpus):
            s = 0.0
            tf_map = Counter(doc_tokens)
            dl = self.doc_len[i]
            for qt in qtokens:
                tf = tf_map.get(qt, 0)
                if tf == 0:
                    continue
                df = self.doc_freq.get(qt, 0)
                idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)
                num = tf * (self.k1 + 1)
                den = tf + self.k1 * (1 - self.b + self.b * dl / max(self.avgdl, 1))
                s += idf * num / den
            scores.append((i, s))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores


def _load_csv(filepath: Path) -> list:
    rows = []
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                rows.append(row)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found", file=sys.stderr)
    return rows


def detect_domain(query: str) -> str:
    """Auto-detect search domain via substring matching (safe for CJK)."""
    q_lower = query.lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in q_lower)
        if count > 0:
            scores[domain] = count
    return max(scores, key=scores.get) if scores else 'tool'


class BiomedSearch:
    """Main search engine for bioinformatics knowledge base."""

    def __init__(self):
        self._cache = {}

    def _get_engine(self, domain: str):
        if domain in self._cache:
            return self._cache[domain]
        config = CSV_CONFIG.get(domain)
        if not config:
            raise ValueError(f"Unknown domain: {domain}. Choose from: {AVAILABLE_DOMAINS}")
        rows = _load_csv(config['file'])
        if not rows:
            self._cache[domain] = (rows, None)
            return rows, None
        docs = [' '.join(row.get(col, '') for col in config['search_cols']) for row in rows]
        bm25 = BM25()
        bm25.fit(docs)
        self._cache[domain] = (rows, bm25)
        return rows, bm25

    def search(self, query: str, domain: Optional[str] = None, max_results: int = 5) -> list:
        if domain is None:
            domain = detect_domain(query)
        rows, bm25 = self._get_engine(domain)
        if not bm25:
            return []
        scores = bm25.score(query)
        config = CSV_CONFIG[domain]
        results = []
        for idx, score in scores[:max_results]:
            if score <= 0:
                break
            result = {'_domain': domain, '_score': round(score, 4)}
            for col in config['output_cols']:
                result[col] = rows[idx].get(col, '')
            # Add actionable handoff info
            skill_name = result.get('Skill_Name', '')
            if skill_name:
                result['_skill_dir'] = str(Path.home() / '.claude' / 'skills' / skill_name)
                result['_next_action'] = f'Invoke skill: {skill_name}'
            results.append(result)
        return results

    def search_all_domains(self, query: str, max_results: int = 3) -> dict:
        all_results = {}
        for domain in ['database', 'tool', 'workflow', 'experiment']:
            results = self.search(query, domain=domain, max_results=max_results)
            if results:
                all_results[domain] = results
        return all_results
