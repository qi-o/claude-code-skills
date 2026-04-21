---
name: biomed-search
description: >
  Bioinformatics knowledge discovery engine. Search across databases, tools,
  workflows, experiment types, and reasoning rules. Use when the user is
  unsure which tool or database to use, wants tool recommendations, or needs
  a complete analysis pipeline generated.
  Triggers: 哪个工具适合, 推荐数据库, 生信工具搜索, 工具推荐,
  如何做单细胞分析, 差异表达用什么工具, 通路分析推荐,
  生成分析流程, generate pipeline, tool recommendation,
  which database for, which tool for, bioinformatics search
---

# BiomedSearch — Bioinformatics Knowledge Discovery

Unified search and routing layer for 24 bioinformatics skills. Discovers the right tools, databases, and workflows for any biomedical analysis task.

## When to Use

**Discovery queries** — when the user needs to FIND the right resource:
- "哪个工具适合差异表达分析"
- "推荐一个通路富集的数据库"
- "如何做单细胞分析"
- "生成一个变异注释的分析流程"
- "which tool should I use for scRNA-seq"
- "generate pipeline for metabolomics"

**NOT for** direct execution — "KEGG通路查询", "差异表达分析", "单细胞聚类" are handled by execution skills directly.

## Quick Start

```bash
# Search for tools (auto-detects domain)
python ~/.claude/skills/biomed-search/scripts/biomed_search.py "差异表达分析"

# Search specific domain
python ~/.claude/skills/biomed-search/scripts/biomed_search.py "单细胞" --domain tool

# Search all domains
python ~/.claude/skills/biomed-search/scripts/biomed_search.py "代谢组学" --all

# Generate full analysis pipeline with reasoning
python ~/.claude/skills/biomed-search/scripts/biomed_search.py "单细胞RNA-seq差异表达分析" --pipeline

# Output formats
python ~/.claude/skills/biomed-search/scripts/biomed_search.py "KEGG通路" --format json
python ~/.claude/skills/biomed-search/scripts/biomed_search.py "GWAS" --format markdown

# Save pipeline to file
python ~/.claude/skills/biomed-search/scripts/biomed_search.py "bulk RNA-seq" --pipeline --persist my-project
```

## Search Domains

| Domain | Flag | Contents |
|--------|------|----------|
| `database` | `--domain database` | 20 bio-databases (KEGG, ClinVar, UniProt, etc.) |
| `tool` | `--domain tool` | 17 analysis tools (Scanpy, PyDESeq2, etc.) |
| `workflow` | `--domain workflow` | 15 research workflows (scRNA-seq pipeline, etc.) |
| `experiment` | `--domain experiment` | 14 experiment types (Bulk RNA-seq, WGS, etc.) |
| `reasoning` | `--domain reasoning` | 10 reasoning rule sets (anti-patterns, decision rules) |

Domain is auto-detected from query keywords. Use `--domain` to override.

## Pipeline Generator

The `--pipeline` flag triggers a 5-step reasoning pipeline:

1. **Classify experiment** — BM25 search on experiment-types.csv
2. **Match reasoning rules** — lookup by experiment category (anti-patterns, key parameters, decision rules)
3. **Multi-domain search** — parallel search across tools + databases + workflows with priority boosting
4. **Deduplicate** — remove duplicate canonical_ids across domains
5. **Assemble pipeline** — output with Installed/External flags and actionable skill handoffs

## Output Fields

Each search result includes:
- `canonical_id` — stable cross-CSV join key
- `_score` — BM25 relevance score (only results > 0)
- `Installed` — `yes` (has skill) or `external` (no local skill)
- `_next_action` — actionable handoff (e.g., "Invoke skill: scanpy")
- `_skill_dir` — full path to the skill directory

## Integration with Other Skills

Search results contain `Skill_Name` and `_skill_dir` fields for direct handoff:

| Search Result | Handoff |
|---------------|---------|
| PyDESeq2 (Installed) | Invoke `pydeseq2` skill |
| KEGG (Installed) | Invoke `kegg-database` skill |
| Scanpy (Installed) | Invoke `scanpy` skill |
| bcftools (External) | Install or use directly |
| PubMed (External) | Use `ai4scholar` MCP |

## Architecture

```
User Query (CN/EN) → biomed_search.py
  ├── detect_domain() → substring matching
  └── core.py BM25 Engine
       ├── Mixed tokenizer (CJK phrase dict + Latin terms)
       ├── BM25 top-N with score > 0 guard
       └── CSV knowledge base (5 domains)
  → Results with skill handoff
  └── pipeline_generator.py (--pipeline)
       → 5-step reasoning with anti-patterns + decision rules
```

Zero external dependencies — Python stdlib only. BM25 engine runs in <50ms for the knowledge base size.
