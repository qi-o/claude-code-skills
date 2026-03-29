---
name: geo-database
description: |
  Access NCBI GEO for gene expression/genomics data. Search/download microarray and RNA-seq datasets (GSE, GSM, GPL), retrieve SOFT/Matrix files, for transcriptomics and expression analysis.
  触发场景：
  (1) 用户需要下载基因表达数据集、查找公开转录组数据
  (2) 用户说"GEO数据库"、"GSE数据集"、"基因表达数据"、"转录组数据下载"、"microarray数据"、"公共数据集"
  (3) 用户需要搜索特定疾病/物种的表达谱、下载 Series Matrix 文件
  Do NOT use for gene annotation queries (use gene-database instead); for differential expression analysis (use pydeseq2 instead).
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# GEO Database

## Overview

The Gene Expression Omnibus (GEO) is NCBI's public repository for high-throughput gene expression and functional genomics data. GEO contains over 264,000 studies with more than 8 million samples from both array-based and sequence-based experiments.

## When to Use This Skill

Use when searching for gene expression datasets, retrieving experimental data, downloading raw and processed files, querying expression profiles, or integrating GEO data into computational analysis workflows.

## GEO Data Organization

| Accession | Description | Count |
|-----------|-------------|-------|
| **GSE** (Series) | Complete experiment with related samples | 264,928+ |
| **GSM** (Sample) | Single experimental sample or biological replicate | 8,068,632+ |
| **GPL** (Platform) | Microarray or sequencing platform used | 27,739+ |
| **GDS** (DataSet) | Curated collections with consistent formatting | 4,348 |
| **Profiles** | Gene-specific expression data linked to sequence features | — |

## Core Capabilities

| Capability | Primary Tool | When to Use |
|-----------|-------------|-------------|
| Search datasets | `Entrez.esearch(db="gds")` | Find studies by keyword/organism/condition |
| Search gene profiles | `Entrez.esearch(db="geoprofiles")` | Find gene-specific expression patterns |
| Download & parse series | `GEOparse.get_GEO()` | Get expression matrix + metadata |
| Batch metadata fetch | E-utilities `esummary` | Multiple accessions at once |
| Bulk file download | FTP / wget | Large files, supplementary data |
| Quick analysis | GEO2R web tool | Exploratory DE analysis without coding |

## Quick Start

```python
import GEOparse
from Bio import Entrez

# Required: set email for NCBI access
Entrez.email = "your.email@example.com"

# Download and parse a GEO Series
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# Get expression matrix
expression_df = gse.pivot_samples('VALUE')  # genes x samples

# Search for datasets
handle = Entrez.esearch(db="gds", term="breast cancer[MeSH] AND Homo sapiens[Organism]")
results = Entrez.read(handle)
```

## Installation

```bash
uv pip install GEOparse biopython pandas numpy scipy matplotlib seaborn statsmodels
```

## Rate Limiting

| Access Method | Rate Limit | Notes |
|--------------|-----------|-------|
| E-utilities (no API key) | 3 req/sec | `time.sleep(0.34)` between calls |
| E-utilities (with API key) | 10 req/sec | `time.sleep(0.1)` between calls |
| FTP | No limit | Preferred for bulk downloads |

Get API key: https://www.ncbi.nlm.nih.gov/account/

## Key Concepts

- **SOFT**: GEO's primary text-based format, easily parsed by GEOparse
- **Series Matrix**: Tab-delimited expression matrix — fastest format for expression data
- **MINiML**: XML format for programmatic access
- **MIAME Compliance**: Standardized annotation enforced for all GEO submissions
- **Platform Annotation**: Maps probe/feature IDs to genes — essential for biological interpretation

## Common Pitfalls

- Different platforms use different probe IDs (requires annotation mapping)
- Expression values may be raw, normalized, or log-transformed — always check metadata
- Sample metadata can be inconsistently formatted across studies
- Not all series have series matrix files (older submissions)
- Platform annotations may be outdated (genes renamed, IDs deprecated)
- Series matrix files can be >1 GB for large studies — plan disk space accordingly

## Use Cases

- **Transcriptomics**: Download expression data, compare profiles, identify DEGs, meta-analysis
- **Drug Response**: Analyze expression changes after treatment, identify biomarkers
- **Disease Biology**: Study disease vs. normal tissues, identify expression signatures
- **Biomarker Discovery**: Screen diagnostic/prognostic markers, validate across cohorts

## GEO2R Web Tool

For quick analysis without coding: https://www.ncbi.nlm.nih.gov/geo/geo2r/?acc=GSExxxxx

Performs differential expression analysis and generates R scripts for reproducibility.

## Resources

- GEO Website: https://www.ncbi.nlm.nih.gov/geo/
- GEOparse Docs: https://geoparse.readthedocs.io/
- E-utilities Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- GEO FTP: ftp://ftp.ncbi.nlm.nih.gov/geo/
- Citation: Barrett et al. (2013) Nucleic Acids Research

## Reference File

All Python code examples are in `references/geo_reference.md`, including:
- GEO DataSets and Profiles search functions
- GEOparse: get_GEO, pivot_samples, supplementary files, filtering
- E-utilities: search/fetch/batch metadata workflows
- FTP download via ftplib and wget/curl
- Quality control and log transformation
- Differential expression analysis with BH correction
- Correlation heatmap and hierarchical clustering
- Batch processing multiple datasets
- Meta-analysis across studies

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 429 | Rate limited | Wait and retry with exponential backoff (0.34s without API key, 0.1s with key) |
| 404 | Not found | Verify GEO accession exists; check GSE/GSM/GPL format |
| 500/502/503 | Server error | Retry up to 3 times with backoff |
| Timeout | Network issue | Retry with longer timeout; consider FTP for bulk downloads |

### Retry Strategy
- Max retries: 3
- Backoff: exponential (0.34s → 0.68s → 1.36s without API key; 0.1s → 0.2s → 0.4s with key)
- On 429: respect rate limits (3 req/s without key, 10 req/s with key)

### Common Pitfalls
- Batch queries: NCBI E-utilities limits to ~10,000 results per search
- Large files: Series Matrix files can exceed 1 GB; use FTP for downloads
- Rate limits: Without API key: 3 req/s; with key: 10 req/s
- Missing annotations: Platform mappings may be outdated; verify gene symbols
- Inconsistent metadata: Sample annotation varies across studies
