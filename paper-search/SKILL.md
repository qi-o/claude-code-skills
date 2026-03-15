---
name: paper-search
description: |
  学术论文搜索与下载工具。支持 arXiv、PubMed、bioRxiv、medRxiv、Google Scholar、Semantic Scholar、CrossRef、IACR 等学术数据库。
  触发场景：
  (1) 用户需要搜索学术论文、文献
  (2) 用户提到 arXiv、PubMed、bioRxiv 等学术数据库
  (3) 用户说"搜索论文"、"查找文献"、"下载论文"
  (4) 用户进行学术调研需要专业数据库支持
  (5) 与 deep-research skill 配合使用，提供 L1 级别学术资料
  基于 openags/paper-search-mcp 转换，无需 MCP 配置。
  Do NOT use for clinical trial searches (use clinicaltrials-database instead) or general web searches (use ducksearch instead).
github_url: https://github.com/openags/paper-search-mcp
github_hash: cf2697fd04a7b7c1ced0e382ab84f0c214614f83
license: MIT
allowed-tools: "Bash(python:*) WebFetch Read Write"
version: 1.0.0
metadata:
  category: research-knowledge
---

# Paper Search - 学术论文搜索工具

从多个学术数据库搜索和下载论文，无需 MCP 配置。

## 支持的数据库

| 数据库 | 搜索 | 下载 | 说明 |
|--------|------|------|------|
| **arXiv** | ✅ | ✅ | 预印本，物理/数学/CS/AI |
| **PubMed** | ✅ | ❌ | 生物医学文献 |
| **bioRxiv** | ✅ | ✅ | 生物学预印本 |
| **medRxiv** | ✅ | ✅ | 医学预印本 |
| **Google Scholar** | ✅ | ❌ | 综合学术搜索 |
| **Semantic Scholar** | ✅ | ✅ | AI 驱动的学术搜索 |
| **CrossRef** | ✅ | ❌ | DOI 元数据库 |
| **IACR** | ✅ | ✅ | 密码学论文 |

## 快速使用

### 搜索论文

```bash
# 搜索 arXiv
python scripts/search.py arxiv "large language model" --max 10

# 搜索 PubMed（医学）
python scripts/search.py pubmed "cancer immunotherapy" --max 10

# 搜索 bioRxiv（生物学预印本）
python scripts/search.py biorxiv "CRISPR gene editing" --max 10

# 搜索 Semantic Scholar
python scripts/search.py semantic "transformer architecture" --max 10

# 搜索 CrossRef（通过 DOI 数据库）
python scripts/search.py crossref "climate change" --max 10
```

### 下载论文 PDF

```bash
# 下载 arXiv 论文
python scripts/download.py arxiv 2301.07041 --output ./papers

# 下载 bioRxiv 论文
python scripts/download.py biorxiv 10.1101/2023.01.01.123456 --output ./papers

# 下载 IACR 论文
python scripts/download.py iacr 2023/123 --output ./papers
```

### 通过 DOI 获取论文信息

```bash
python scripts/search.py doi 10.1038/nature12373
```

## 输出格式

搜索结果以 JSON 格式输出，包含：

```json
{
  "paper_id": "2301.07041",
  "title": "Paper Title",
  "authors": ["Author 1", "Author 2"],
  "abstract": "Abstract text...",
  "url": "https://arxiv.org/abs/2301.07041",
  "pdf_url": "https://arxiv.org/pdf/2301.07041.pdf",
  "published_date": "2023-01-17",
  "source": "arxiv",
  "categories": ["cs.CL", "cs.AI"],
  "doi": "10.48550/arXiv.2301.07041"
}
```

## 与 deep-research 配合使用

在 `deep-research` 的 Step 2（资料分层）中，使用本 skill 获取 L1 级别学术资料：

```markdown
## 资料分层建议

| 层级 | 资料类型 | 获取方式 |
|------|----------|----------|
| **L1** | arXiv 预印本、PubMed 论文 | 使用 paper-search skill |
| **L2** | 官方博客、技术演讲 | WebSearch |
| **L3** | 权威媒体、专家解读 | WebSearch |
| **L4** | 社区讨论、个人博客 | WebSearch |
```

## 与 deep-research 深度集成

### 作为第七轮搜索策略

在 `deep-research` 的 7 轮搜索策略中，本 skill 负责第七轮「学术前沿搜索」：

```markdown
## 第七轮搜索执行流程

1. **判断是否需要学术搜索**：
   - 主题涉及科学原理、算法、技术机制 → 必须执行
   - 需要引用学术论文支撑结论 → 必须执行
   - 用户明确要求学术文献支持 → 必须执行

2. **选择合适的数据库**：
   | 领域 | 推荐数据库 | 命令 |
   |------|-----------|------|
   | AI/机器学习/深度学习 | arXiv | `python scripts/search.py arxiv "<关键词>" --max 10` |
   | 计算机科学/算法 | arXiv + Semantic Scholar | 两者都搜索 |
   | 生物医学/临床 | PubMed + bioRxiv | 两者都搜索 |
   | 跨领域综合 | Semantic Scholar | `python scripts/search.py semantic "<关键词>" --max 10` |
   | 密码学/安全 | IACR | `python scripts/search.py iacr "<关键词>" --max 10` |

3. **资料归类**：
   - 所有学术论文自动归类为 **L1 级别**
   - 在 `01_资料来源.md` 中标注来源数据库和论文 ID
```

### 学术资料记录模板

在 deep-research 的 `01_资料来源.md` 中，学术论文应使用以下格式：

```markdown
## 资料 #[序号] (学术论文)
- **标题**：[论文标题]
- **作者**：[作者列表]
- **来源**：arXiv / PubMed / bioRxiv / Semantic Scholar
- **ID**：arXiv:2301.07041 / PMID:12345678 / DOI:10.xxxx
- **链接**：[URL]
- **层级**：L1（学术论文）
- **发布日期**：[YYYY-MM-DD]
- **摘要**：[论文摘要]
- **与子问题关联**：[对应哪个子问题]
```

### 搜索关键词策略

为获得最佳搜索结果，建议：

1. **使用英文关键词**：学术数据库以英文为主
2. **组合多个关键词**：`"transformer attention mechanism"`
3. **使用领域术语**：避免过于通俗的表述
4. **限制时间范围**：对于快速发展的领域，优先搜索近 2 年的论文

## 依赖安装

```bash
pip install requests feedparser PyPDF2 scholarly httpx beautifulsoup4
```

## 常见问题

### Google Scholar 被限制
Google Scholar 有反爬机制，频繁请求可能被限制。建议：
- 降低请求频率
- 使用代理
- 优先使用 Semantic Scholar 替代

### PubMed 无法下载 PDF
PubMed 是索引数据库，不直接提供 PDF。可以：
- 使用论文的 DOI 到出版商网站下载
- 检查 PubMed Central (PMC) 是否有免费全文

### Semantic Scholar API Key
可选配置 API Key 获得更高配额：
```bash
export SEMANTIC_SCHOLAR_API_KEY="your_key"
```

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 与 deep-research 配合时作为第七轮搜索策略
- 搜索结果自动归类为 L1 级别学术资料

### Custom Instruction Injection

学术搜索建议使用英文关键词以获得更好结果