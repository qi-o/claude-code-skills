---
name: qpcr-graphpad-formatter
description: Format qPCR data for GraphPad Prism. Use when the user has qPCR data in CSV format and wants to convert it to a two-column format (LC and KO) with fold change values calculated using the 2^-ΔΔCt method, ready for direct copy-paste into GraphPad Prism. Use when user says "qPCR数据", "GraphPad", "Ct值转换", "fold change", or "qPCR格式化". Do NOT use for general data visualization (use pub-figures instead) or non-qPCR data.
license: MIT
allowed-tools: "Bash(python:*) Read Write"
version: 0.1.0
metadata:
  category: domain-specific
---

# QPCR Data Formatter for GraphPad Prism

This skill converts qPCR data from CSV format to a two-column layout ready for GraphPad Prism.

## When to Use This Skill

Use this skill when:
- User has qPCR data with Ct values in CSV format
- User wants to import data into GraphPad Prism
- User needs fold change calculations (2^-螖螖Ct method)
- Output should be LC and KO columns with tab-separated values

## Workflow

### 1. Verify Input Data

Ensure the CSV file contains these columns:
- `Sample`: Unique sample identifier
- `Group`: Experimental group (e.g., siNC for control, siGene for treatment)
- `Gene`: Gene names (reference genes + target genes)
- `TechRep`: Technical replicate number
- `Ct`: Ct values

### 2. Run the Formatter Script

Execute the script to process the data:

```bash
python scripts/qpcr_to_graphpad.py <csv_file>
```

The script automatically:
- Calculates average Ct for technical replicates
- Computes 螖Ct using reference genes (default: RPLP0, HPRT1)
- Computes 螖螖Ct relative to control group (default: siNC)
- Calculates Fold Change = 2^(-螖螖Ct)
- Formats output as LC/KO columns

### 3. Output Format

For each target gene, the output shows:

```
GENE_NAME:
LC    KO
1.37    0.18
0.86    0.15
0.85    0.12
```

- `LC` column: Control group (siNC) fold changes
- `KO` column: Treatment group fold changes
- Tab-separated for easy copy-paste
- Three rows = three biological replicates

### 4. Copy to GraphPad Prism

1. Open the generated `GraphPad_Prism_Data.txt` file
2. Select the LC/KO data for a gene
3. Copy and paste directly into GraphPad Prism
4. Create bar graph with mean 卤 SEM

## Script Options

The formatter script accepts:

```bash
python scripts/qpcr_to_graphpad.py <csv_file> [--control GROUP] [--ref GENES] [--targets GENES]
```

Arguments:
- `csv_file`: Path to qPCR data CSV file (required)
- `--control`: Control group name (default: siNC)
- `--ref`: Reference genes comma-separated (default: RPLP0,HPRT1)
- `--targets`: Target genes comma-separated (default: auto-detect all non-reference genes)

## Output File

Data is saved to `GraphPad_Prism_Data.txt` in the same directory as the input CSV file.

## Data Interpretation

- Fold change 鈮?1.0: No change (baseline)
- Fold change > 1.0: Upregulation
- Fold change < 1.0: Downregulation
- Values represent biological replicates (n=3 typical)
