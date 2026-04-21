# BiomedSearch Quick Reference

## Domain Routing Keywords

| Domain | Chinese Triggers | English Triggers |
|--------|-----------------|-----------------|
| database | 数据库, 通路数据库, 变异数据库 | kegg, clinvar, ensembl, uniprot, pdb |
| tool | 工具, 分析工具, 可视化, 软件 | scanpy, pydeseq2, biopython, deseq2 |
| workflow | 流程, 工作流, 分析流程, 全流程 | pipeline, complete pipeline, workflow |
| experiment | 单细胞, 转录组, 全基因组, 代谢组 | rna-seq, scrna-seq, wgs, proteomics |
| reasoning | 推理, 决策, 规则, 反模式, 参数 | reasoning, decision, rule, anti-pattern |

## Example Queries

### Tool Discovery
```bash
python biomed_search.py "差异表达用什么工具"
python biomed_search.py "which tool for single cell clustering"
python biomed_search.py "蛋白质结构预测工具" --domain tool
```

### Database Discovery
```bash
python biomed_search.py "推荐一个通路富集数据库"
python biomed_search.py "clinical variant database"
python biomed_search.py "代谢组学数据库" --domain database
```

### Pipeline Generation
```bash
python biomed_search.py "单细胞RNA-seq分析" --pipeline
python biomed_search.py "GWAS全基因组关联" --pipeline --format json
python biomed_search.py "bulk RNA-seq差异表达" --pipeline --persist my-rna-seq
```

## Canonical ID Reference

### Databases (db-*)
`db-kegg`, `db-reactome`, `db-clinvar`, `db-ensembl`, `db-opentargets`, `db-string`, `db-uniprot`, `db-pdb`, `db-alphafold`, `db-drugbank`, `db-hmdb`, `db-geo`, `db-gene`, `db-clinicaltrials`, `db-pubmed`, `db-biorxiv`, `db-semantic-scholar`, `db-go`, `db-gnomad`, `db-clingen`

### Tools (tool-*)
`tool-scanpy`, `tool-pydeseq2`, `tool-biopython`, `tool-anndata`, `tool-bioservices`, `tool-matplotlib`, `tool-bcftools`, `tool-pydicom`, `tool-qpcr`, `tool-pubfigures`, `tool-samtools`, `tool-fastqc`, `tool-multiqc`, `tool-bedtools`, `tool-star`, `tool-gatk`, `tool-macs2`

### Workflows (wf-*)
`wf-scrna-seq`, `wf-bulk-de`, `wf-variant-annot`, `wf-pathway-enrich`, `wf-protein-struct`, `wf-drug-target`, `wf-metabolomics`, `wf-gwas`, `wf-chipseq`, `wf-atacseq`, `wf-clinvar-interp`, `wf-rna-seq-full`, `wf-ppi-network`, `wf-qpcr-validation`, `wf-medical-imaging`

### Experiments (exp-*)
`exp-bulk-rna`, `exp-scrna-seq`, `exp-wgs`, `exp-wes`, `exp-gwas`, `exp-proteomics`, `exp-metabolomics`, `exp-chipseq`, `exp-atacseq`, `exp-struct-pred`, `exp-drug-target`, `exp-clinvar`, `exp-qpcr`, `exp-imaging`

### Reasoning (reason-*)
`reason-transcriptomics`, `reason-genomics`, `reason-systems`, `reason-structural`, `reason-pharmacology`, `reason-metabolomics`, `reason-epigenomics`, `reason-clinical`, `reason-validation`, `reason-imaging`
