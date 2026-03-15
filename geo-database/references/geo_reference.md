# GEO Database 完整代码参考

## 目录

1. [搜索 GEO 数据](#搜索-geo-数据)
2. [GEOparse 使用](#geoparse-使用)
3. [E-utilities 访问](#e-utilities-访问)
4. [FTP 直接下载](#ftp-直接下载)
5. [质量控制与预处理](#质量控制与预处理)
6. [差异表达分析](#差异表达分析)
7. [聚类分析](#聚类分析)
8. [批量处理多数据集](#批量处理多数据集)
9. [元分析](#元分析)
10. [安装与配置](#安装与配置)

---

## 搜索 GEO 数据

### GEO DataSets 搜索

```python
from Bio import Entrez

Entrez.email = "your.email@example.com"

def search_geo_datasets(query, retmax=20):
    """Search GEO DataSets database"""
    handle = Entrez.esearch(
        db="gds",
        term=query,
        retmax=retmax,
        usehistory="y"
    )
    results = Entrez.read(handle)
    handle.close()
    return results

# 示例搜索
results = search_geo_datasets("breast cancer[MeSH] AND Homo sapiens[Organism]")
print(f"Found {results['Count']} datasets")

results = search_geo_datasets("GPL570[Accession]")
results = search_geo_datasets("expression profiling by array[DataSet Type]")
```

### GEO Profiles 搜索

```python
def search_geo_profiles(gene_name, organism="Homo sapiens", retmax=100):
    """Search GEO Profiles for a specific gene"""
    query = f"{gene_name}[Gene Name] AND {organism}[Organism]"
    handle = Entrez.esearch(
        db="geoprofiles",
        term=query,
        retmax=retmax
    )
    results = Entrez.read(handle)
    handle.close()
    return results

tp53_results = search_geo_profiles("TP53", organism="Homo sapiens")
print(f"Found {tp53_results['Count']} expression profiles for TP53")
```

### 高级搜索

```python
def advanced_geo_search(terms, operator="AND"):
    """Build complex search queries"""
    query = f" {operator} ".join(terms)
    return search_geo_datasets(query)

# 最近的 RNA-seq 研究
search_terms = [
    "RNA-seq[DataSet Type]",
    "Homo sapiens[Organism]",
    "2024[Publication Date]"
]
results = advanced_geo_search(search_terms)

# 按作者和疾病搜索
results = advanced_geo_search(["Smith[Author]", "diabetes[Disease]"])
```

---

## GEOparse 使用

### 基础用法

```python
import GEOparse

# 下载并解析 GEO Series
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# 访问系列元数据
print(gse.metadata['title'])
print(gse.metadata['summary'])
print(gse.metadata['overall_design'])

# 访问样本信息
for gsm_name, gsm in gse.gsms.items():
    print(f"Sample: {gsm_name}")
    print(f"  Title: {gsm.metadata['title'][0]}")
    print(f"  Source: {gsm.metadata['source_name_ch1'][0]}")
    print(f"  Characteristics: {gsm.metadata.get('characteristics_ch1', [])}")

# 访问平台信息
for gpl_name, gpl in gse.gpls.items():
    print(f"Platform: {gpl_name}")
    print(f"  Title: {gpl.metadata['title'][0]}")
    print(f"  Organism: {gpl.metadata['organism'][0]}")
```

### 提取表达矩阵

```python
import GEOparse
import pandas as pd

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# 方法1：从 series matrix 文件（最快）
if hasattr(gse, 'pivot_samples'):
    expression_df = gse.pivot_samples('VALUE')
    print(expression_df.shape)  # genes x samples

# 方法2：从单个样本
expression_data = {}
for gsm_name, gsm in gse.gsms.items():
    if hasattr(gsm, 'table'):
        expression_data[gsm_name] = gsm.table['VALUE']

expression_df = pd.DataFrame(expression_data)
print(f"Expression matrix: {expression_df.shape}")
```

### 下载补充文件

```python
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

gse.download_supplementary_files(
    directory="./data/GSE123456_suppl",
    download_sra=False  # 设为 True 下载 SRA 文件
)

# 列出可用补充文件
for gsm_name, gsm in gse.gsms.items():
    if hasattr(gsm, 'supplementary_files'):
        print(f"Sample {gsm_name}:")
        for file_url in gsm.metadata.get('supplementary_file', []):
            print(f"  {file_url}")
```

### 过滤和子集

```python
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# 按元数据过滤样本
control_samples = [
    gsm_name for gsm_name, gsm in gse.gsms.items()
    if 'control' in gsm.metadata.get('title', [''])[0].lower()
]

treatment_samples = [
    gsm_name for gsm_name, gsm in gse.gsms.items()
    if 'treatment' in gsm.metadata.get('title', [''])[0].lower()
]

# 提取子集表达矩阵
expression_df = gse.pivot_samples('VALUE')
control_expr = expression_df[control_samples]
treatment_expr = expression_df[treatment_samples]
```

---

## E-utilities 访问

### 基础工作流

```python
from Bio import Entrez
import time

Entrez.email = "your.email@example.com"

def search_geo(query, db="gds", retmax=100):
    handle = Entrez.esearch(db=db, term=query, retmax=retmax, usehistory="y")
    results = Entrez.read(handle)
    handle.close()
    return results

def fetch_geo_summaries(id_list, db="gds"):
    ids = ",".join(id_list)
    handle = Entrez.esummary(db=db, id=ids)
    summaries = Entrez.read(handle)
    handle.close()
    return summaries

def fetch_geo_records(id_list, db="gds"):
    ids = ",".join(id_list)
    handle = Entrez.efetch(db=db, id=ids, retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    return records

# 示例工作流
search_results = search_geo("breast cancer AND Homo sapiens")
id_list = search_results['IdList'][:5]

summaries = fetch_geo_summaries(id_list)
for summary in summaries:
    print(f"GDS: {summary.get('Accession', 'N/A')}")
    print(f"Title: {summary.get('title', 'N/A')}")
    print(f"Samples: {summary.get('n_samples', 'N/A')}")
```

### 批量获取元数据

```python
def batch_fetch_geo_metadata(accessions, batch_size=100):
    """Fetch metadata for multiple GEO accessions"""
    results = {}

    for i in range(0, len(accessions), batch_size):
        batch = accessions[i:i + batch_size]

        for accession in batch:
            try:
                query = f"{accession}[Accession]"
                search_handle = Entrez.esearch(db="gds", term=query)
                search_results = Entrez.read(search_handle)
                search_handle.close()

                if search_results['IdList']:
                    summary_handle = Entrez.esummary(
                        db="gds",
                        id=search_results['IdList'][0]
                    )
                    summary = Entrez.read(summary_handle)
                    summary_handle.close()
                    results[accession] = summary[0]

                time.sleep(0.34)  # 最多 3 请求/秒

            except Exception as e:
                print(f"Error fetching {accession}: {e}")

    return results

gse_list = ["GSE100001", "GSE100002", "GSE100003"]
metadata = batch_fetch_geo_metadata(gse_list)
```

---

## FTP 直接下载

### Python ftplib

```python
import ftplib
import os

def download_geo_ftp(accession, file_type="matrix", dest_dir="./data"):
    """Download GEO files via FTP"""
    if accession.startswith("GSE"):
        gse_num = accession[3:]
        base_num = gse_num[:-3] + "nnn"
        ftp_path = f"/geo/series/GSE{base_num}/{accession}/"

        if file_type == "matrix":
            filename = f"{accession}_series_matrix.txt.gz"
        elif file_type == "soft":
            filename = f"{accession}_family.soft.gz"
        elif file_type == "miniml":
            filename = f"{accession}_family.xml.tgz"

    ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
    ftp.login()
    ftp.cwd(ftp_path)

    os.makedirs(dest_dir, exist_ok=True)
    local_file = os.path.join(dest_dir, filename)

    with open(local_file, 'wb') as f:
        ftp.retrbinary(f'RETR {filename}', f.write)

    ftp.quit()
    print(f"Downloaded: {local_file}")
    return local_file

download_geo_ftp("GSE123456", file_type="matrix")
download_geo_ftp("GSE123456", file_type="soft")
```

### wget/curl 命令

```bash
# 下载 series matrix 文件
wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/matrix/GSE123456_series_matrix.txt.gz

# 下载所有补充文件
wget -r -np -nd ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/suppl/

# 下载 SOFT 格式文件
wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/soft/GSE123456_family.soft.gz
```

---

## 质量控制与预处理

```python
import GEOparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")
expression_df = gse.pivot_samples('VALUE')

# 检查缺失值
print(f"Missing values: {expression_df.isnull().sum().sum()}")

# Log 转换（如需要）
if expression_df.min().min() > 0:
    if expression_df.max().max() > 100:
        expression_df = np.log2(expression_df + 1)
        print("Applied log2 transformation")

# 分布图
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
expression_df.plot.box(ax=plt.gca())
plt.title("Expression Distribution per Sample")
plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
expression_df.mean(axis=1).hist(bins=50)
plt.title("Gene Expression Distribution")
plt.xlabel("Average Expression")

plt.tight_layout()
plt.savefig("geo_qc.png", dpi=300, bbox_inches='tight')
```

---

## 差异表达分析

```python
import GEOparse
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")
expression_df = gse.pivot_samples('VALUE')

control_samples = ["GSM1", "GSM2", "GSM3"]
treatment_samples = ["GSM4", "GSM5", "GSM6"]

results = []
for gene in expression_df.index:
    control_expr = expression_df.loc[gene, control_samples]
    treatment_expr = expression_df.loc[gene, treatment_samples]

    fold_change = treatment_expr.mean() - control_expr.mean()
    t_stat, p_value = stats.ttest_ind(treatment_expr, control_expr)

    results.append({
        'gene': gene,
        'log2_fold_change': fold_change,
        'p_value': p_value,
        'control_mean': control_expr.mean(),
        'treatment_mean': treatment_expr.mean()
    })

de_results = pd.DataFrame(results)

# Benjamini-Hochberg 多重检验校正
_, de_results['q_value'], _, _ = multipletests(
    de_results['p_value'],
    method='fdr_bh'
)

# 筛选显著基因
significant_genes = de_results[
    (de_results['q_value'] < 0.05) &
    (abs(de_results['log2_fold_change']) > 1)
]

print(f"Significant genes: {len(significant_genes)}")
significant_genes.to_csv("de_results.csv", index=False)
```

---

## 聚类分析

```python
import GEOparse
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")
expression_df = gse.pivot_samples('VALUE')

# 样本相关性热图
sample_corr = expression_df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(sample_corr, cmap='coolwarm', center=0,
            square=True, linewidths=0.5)
plt.title("Sample Correlation Matrix")
plt.tight_layout()
plt.savefig("sample_correlation.png", dpi=300, bbox_inches='tight')

# 层次聚类
distances = pdist(expression_df.T, metric='correlation')
linkage = hierarchy.linkage(distances, method='average')

plt.figure(figsize=(12, 6))
hierarchy.dendrogram(linkage, labels=expression_df.columns)
plt.title("Hierarchical Clustering of Samples")
plt.xlabel("Samples")
plt.ylabel("Distance")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("sample_clustering.png", dpi=300, bbox_inches='tight')
```

---

## 批量处理多数据集

```python
import GEOparse
import pandas as pd
import os

def batch_download_geo(gse_list, destdir="./geo_data"):
    """Download multiple GEO series"""
    results = {}

    for gse_id in gse_list:
        try:
            print(f"Processing {gse_id}...")
            gse = GEOparse.get_GEO(geo=gse_id, destdir=destdir)

            results[gse_id] = {
                'title': gse.metadata.get('title', ['N/A'])[0],
                'organism': gse.metadata.get('organism', ['N/A'])[0],
                'platform': list(gse.gpls.keys())[0] if gse.gpls else 'N/A',
                'num_samples': len(gse.gsms),
                'submission_date': gse.metadata.get('submission_date', ['N/A'])[0]
            }

            if hasattr(gse, 'pivot_samples'):
                expr_df = gse.pivot_samples('VALUE')
                expr_df.to_csv(f"{destdir}/{gse_id}_expression.csv")
                results[gse_id]['num_genes'] = len(expr_df)

        except Exception as e:
            print(f"Error processing {gse_id}: {e}")
            results[gse_id] = {'error': str(e)}

    summary_df = pd.DataFrame(results).T
    summary_df.to_csv(f"{destdir}/batch_summary.csv")
    return results

gse_list = ["GSE100001", "GSE100002", "GSE100003"]
results = batch_download_geo(gse_list)
```

---

## 元分析

```python
import GEOparse
import pandas as pd
import numpy as np

def meta_analysis_geo(gse_list, gene_of_interest):
    """Perform meta-analysis of gene expression across studies"""
    results = []

    for gse_id in gse_list:
        try:
            gse = GEOparse.get_GEO(geo=gse_id, destdir="./data")
            gpl = list(gse.gpls.values())[0]

            if hasattr(gpl, 'table'):
                gene_probes = gpl.table[
                    gpl.table['Gene Symbol'].str.contains(
                        gene_of_interest, case=False, na=False
                    )
                ]

                if not gene_probes.empty:
                    expr_df = gse.pivot_samples('VALUE')

                    for probe_id in gene_probes['ID']:
                        if probe_id in expr_df.index:
                            expr_values = expr_df.loc[probe_id]
                            results.append({
                                'study': gse_id,
                                'probe': probe_id,
                                'mean_expression': expr_values.mean(),
                                'std_expression': expr_values.std(),
                                'num_samples': len(expr_values)
                            })

        except Exception as e:
            print(f"Error in {gse_id}: {e}")

    return pd.DataFrame(results)

gse_studies = ["GSE100001", "GSE100002", "GSE100003"]
meta_results = meta_analysis_geo(gse_studies, "TP53")
print(meta_results)
```

---

## 安装与配置

```bash
# 主要 GEO 访问库（推荐）
uv pip install GEOparse

# E-utilities 和 NCBI 编程访问
uv pip install biopython

# 数据分析
uv pip install pandas numpy scipy

# 可视化
uv pip install matplotlib seaborn

# 统计分析
uv pip install statsmodels scikit-learn
```

```python
from Bio import Entrez

# 必须设置邮箱（NCBI 要求）
Entrez.email = "your.email@example.com"

# 可选：设置 API key 提升速率限制
# 申请地址：https://www.ncbi.nlm.nih.gov/account/
Entrez.api_key = "your_api_key_here"

# 有 API key：10 请求/秒
# 无 API key：3 请求/秒
```
