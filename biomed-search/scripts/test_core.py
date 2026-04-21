#!/usr/bin/env python3
"""Automated tests for BiomedSearch core engine."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core import BM25, BiomedSearch, detect_domain, CSV_CONFIG, _load_csv, DATA_DIR


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.bm25 = BM25()

    def test_cjk_phrases_preserved(self):
        tokens = self.bm25.tokenize('差异表达分析')
        self.assertIn('差异表达', tokens)

    def test_cjk_phrase_single_cell(self):
        tokens = self.bm25.tokenize('单细胞分析')
        self.assertIn('单细胞', tokens)

    def test_latin_terms_intact(self):
        tokens = self.bm25.tokenize('RNA-seq differential expression')
        self.assertIn('rna-seq', tokens)

    def test_mixed_cjk_latin(self):
        tokens = self.bm25.tokenize('单细胞RNA-seq差异表达分析')
        self.assertIn('单细胞', tokens)
        self.assertIn('rna-seq', tokens)
        self.assertIn('差异表达', tokens)

    def test_empty_input(self):
        self.assertEqual(self.bm25.tokenize(''), [])
        self.assertEqual(self.bm25.tokenize(None), [])

    def test_digits_preserved(self):
        tokens = self.bm25.tokenize('PyDESeq2 DESeq2')
        self.assertIn('pydeseq2', tokens)
        self.assertIn('deseq2', tokens)

    def test_multiple_biomed_phrases(self):
        tokens = self.bm25.tokenize('通路富集与蛋白质结构分析')
        self.assertIn('通路富集', tokens)
        self.assertIn('蛋白质结构', tokens)


class TestDetectDomain(unittest.TestCase):
    def test_database_kegg(self):
        self.assertEqual(detect_domain('KEGG通路查询'), 'database')

    def test_tool_expression(self):
        self.assertEqual(detect_domain('差异表达工具'), 'tool')

    def test_workflow_pipeline(self):
        self.assertEqual(detect_domain('分析流程'), 'workflow')

    def test_experiment_scrna(self):
        self.assertEqual(detect_domain('单细胞RNA-seq'), 'experiment')

    def test_reasoning_rules(self):
        self.assertEqual(detect_domain('推理决策规则'), 'reasoning')

    def test_default_to_tool(self):
        self.assertEqual(detect_domain('random unknown query xyz'), 'tool')


class TestBM25Scoring(unittest.TestCase):
    def setUp(self):
        self.bm25 = BM25()
        self.bm25.fit(['differential expression RNA-seq',
                       'single cell clustering UMAP',
                       'pathway enrichment KEGG'])

    def test_score_positive_for_match(self):
        scores = self.bm25.score('differential expression')
        top_idx, top_score = scores[0]
        self.assertGreater(top_score, 0)

    def test_score_zero_for_no_match(self):
        scores = self.bm25.score('quantum physics unrelated')
        for _, score in scores:
            self.assertLessEqual(score, 0)

    def test_scores_sorted_descending(self):
        scores = self.bm25.score('expression')
        for i in range(len(scores) - 1):
            self.assertGreaterEqual(scores[i][1], scores[i + 1][1])


class TestCSVLoading(unittest.TestCase):
    def test_databases_csv_exists(self):
        rows = _load_csv(DATA_DIR / 'databases.csv')
        self.assertGreater(len(rows), 0)

    def test_tools_csv_exists(self):
        rows = _load_csv(DATA_DIR / 'tools.csv')
        self.assertGreater(len(rows), 0)

    def test_workflows_csv_exists(self):
        rows = _load_csv(DATA_DIR / 'workflows.csv')
        self.assertGreater(len(rows), 0)

    def test_experiments_csv_exists(self):
        rows = _load_csv(DATA_DIR / 'experiment-types.csv')
        self.assertGreater(len(rows), 0)

    def test_reasoning_csv_exists(self):
        rows = _load_csv(DATA_DIR / 'analysis-reasoning.csv')
        self.assertGreater(len(rows), 0)

    def test_missing_file_returns_empty(self):
        rows = _load_csv(DATA_DIR / 'nonexistent.csv')
        self.assertEqual(rows, [])

    def test_canonical_id_present(self):
        for csv_file in ['databases.csv', 'tools.csv', 'workflows.csv',
                         'experiment-types.csv', 'analysis-reasoning.csv']:
            rows = _load_csv(DATA_DIR / csv_file)
            for row in rows:
                self.assertIn('canonical_id', row, f'Missing canonical_id in {csv_file}')
                self.assertTrue(row['canonical_id'], f'Empty canonical_id in {csv_file}')


class TestBiomedSearch(unittest.TestCase):
    def setUp(self):
        self.engine = BiomedSearch()

    def test_tool_search_pydeseq2(self):
        results = self.engine.search('差异表达分析', domain='tool', max_results=3)
        names = [r.get('Tool_Name', '') for r in results]
        self.assertTrue(any('PyDESeq2' in n for n in names),
                        f'PyDESeq2 not found in top results: {names}')

    def test_database_search_kegg(self):
        results = self.engine.search('pathway enrichment', domain='database', max_results=3)
        names = [r.get('Database_Name', '') for r in results]
        self.assertTrue(any('KEGG' in n for n in names),
                        f'KEGG not found in top results: {names}')

    def test_chinese_query_metabolomics(self):
        results = self.engine.search('代谢组学', domain='database', max_results=3)
        names = [r.get('Database_Name', '') for r in results]
        self.assertTrue(any('HMDB' in n for n in names),
                        f'HMDB not found for 代谢组学: {names}')

    def test_score_filter(self):
        results = self.engine.search('差异表达分析', domain='tool')
        for r in results:
            self.assertGreater(r['_score'], 0)

    def test_no_results_returns_empty(self):
        results = self.engine.search('quantum physics xyzzy', domain='tool')
        self.assertEqual(results, [])

    def test_domain_in_results(self):
        results = self.engine.search('差异表达', domain='tool', max_results=1)
        if results:
            self.assertEqual(results[0]['_domain'], 'tool')

    def test_search_all_domains(self):
        all_results = self.engine.search_all_domains('差异表达分析', max_results=2)
        self.assertIsInstance(all_results, dict)
        for domain, results in all_results.items():
            self.assertIn(domain, ['database', 'tool', 'workflow', 'experiment'])
            for r in results:
                self.assertGreater(r['_score'], 0)

    def test_handoff_info_present(self):
        results = self.engine.search('差异表达', domain='tool', max_results=1)
        if results and results[0].get('Skill_Name'):
            self.assertIn('_skill_dir', results[0])
            self.assertIn('_next_action', results[0])

    def test_invalid_domain_raises(self):
        with self.assertRaises(ValueError):
            self.engine.search('test', domain='nonexistent')


if __name__ == '__main__':
    unittest.main()
