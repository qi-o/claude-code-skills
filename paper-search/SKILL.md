---
name: paper-search
description: >
  学术论文搜索与下载工具。支持 arXiv、PubMed、bioRxiv、medRxiv、Google Scholar、Semantic Scholar、CrossRef、IACR、OpenAlex、PMC、CORE、Europe PMC、Zenodo、HAL、SSRN 等 20+ 学术数据库。
  触发场景：
  (1) 用户需要搜索学术论文、文献
  (2) 用户提到 arXiv、PubMed、bioRxiv 等学术数据库
  (3) 用户说"搜索论文"、"查找文献"、"下载论文"
  (4) 用户进行学术调研需要专业数据库支持
  (5) 与 deep-research skill 配合使用，提供 L1 级别学术资料
  Triggers (EN): search papers, find papers, download paper, academic search, literature search,
  scholarly articles, research papers, arxiv search, pubmed search, paper download,
  find academic articles, citation search.
  PubMed/arXiv 排序优化、CLI 入口支持。基于 openags/paper-search-mcp 转换，无需 MCP 配置。
  Do NOT use for clinical trial searches (use clinicaltrials-database instead) or general web searches (use ducksearch instead).
github_url: https://github.com/openags/paper-search-mcp
github_hash: 3fc7f633c3c2cecae1569f98f25102d2684e09f7
license: MIT
allowed-tools: "Bash(python:*) WebFetch Read Write"
version: 1.2.0
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
| **Google Scholar** | ⚠️ | ❌ | 综合学术搜索（有反爬，需代理） |
| **Semantic Scholar** | ✅ | ✅(OA) | AI 驱动的学术搜索 |
| **CrossRef** | ✅ | ❌ | DOI 元数据库 |
| **IACR** | ✅ | ✅ | 密码学论文 |
| **OpenAlex** | ✅ | ❌ | 免费开放元数据骨干 |
| **PMC** | ✅ | ✅(OA) | PubMed Central 全文 |
| **CORE** | ✅ | ✅ | 开放获取仓库聚合 |
| **Europe PMC** | ✅ | ✅(OA) | 欧洲生物医学全文 |
| **dblp** | ✅ | ❌ | CS 文献索引 |
| **OpenAIRE** | ✅ | ❌ | 欧洲开放获取 |
| **Zenodo** | ✅ | ✅ | 研究数据/论文仓库 |
| **HAL** | ✅ | ✅ | 法国开放获取平台 |
| **SSRN** | ⚠️ | ⚠️ | 社科/经济预印本 |
| **DOAJ** | ✅ | ⚠️ | 开放获取期刊目录 |
| **Unpaywall** | ✅(DOI) | ❌ | OA 元数据（需邮箱） |
| **IEEE Xplore** | 🚧 | 🚧 | 需 `PAPER_SEARCH_MCP_IEEE_API_KEY` |
| **ACM DL** | 🚧 | 🚧 | 需 `PAPER_SEARCH_MCP_ACM_API_KEY` |

> ✅ 稳定可用  ⚠️ 受上游限制  ❌ 不支持  🚧 需 API Key 激活

## 快速使用

### 多源并发搜索（推荐）

```bash
# 跨多个数据库并发搜索 + 自动去重
python scripts/search.py multi "large language model" --sources arxiv,semantic,openalex --max 10

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

# 搜索 OpenAlex（免费开放元数据）
python scripts/search.py openalex "climate change" --max 10

# 搜索 Zenodo（研究数据/论文）
python scripts/search.py zenodo "RNA sequencing" --max 10
```

### 下载论文 PDF（OA 优先回退链）

```bash
# 自动回退：源站 → OpenAIRE/CORE/PMC → Unpaywall → (可选 Sci-Hub)
python scripts/download.py fallback 10.1038/nature12373 --output ./papers

# 下载 arXiv 论文
python scripts/download.py arxiv 2301.07041 --output ./papers

# 下载 bioRxiv 论文
python scripts/download.py biorxiv 10.1101/2023.01.01.123456 --output ./papers

# 下载 IACR 论文
python scripts/download.py iacr 2023/123 --output ./papers

# 下载 Zenodo 论文
python scripts/download.py zenodo 1234567 --output ./papers
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

## 环境变量配置（可选）

所有变量均为可选，统一使用 `PAPER_SEARCH_MCP_*` 前缀（兼容旧名）：

```bash
# Google Scholar 代理（绕过反爬）
export PAPER_SEARCH_MCP_GOOGLE_SCHOLAR_PROXY_URL="http://your-proxy:port"

# Semantic Scholar（提升速率限制）
export PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY="your_key"

# Unpaywall（启用 DOI OA 元数据查询，必填才能使用）
export PAPER_SEARCH_MCP_UNPAYWALL_EMAIL="your@email.com"

# CORE（推荐，提升速率限制）
export PAPER_SEARCH_MCP_CORE_API_KEY="your_key"

# DOAJ（可选，提升速率限制）
export PAPER_SEARCH_MCP_DOAJ_API_KEY="your_key"

# Zenodo（可选，访问私有记录）
export PAPER_SEARCH_MCP_ZENODO_ACCESS_TOKEN="your_token"

# IEEE Xplore（必填才能激活）
export PAPER_SEARCH_MCP_IEEE_API_KEY="your_key"

# ACM DL（必填才能激活）
export PAPER_SEARCH_MCP_ACM_API_KEY="your_key"
```

## 依赖安装

```bash
pip install requests feedparser PyPDF2 scholarly httpx beautifulsoup4
```

## 常见问题

### Google Scholar 被限制
配置代理变量 `PAPER_SEARCH_MCP_GOOGLE_SCHOLAR_PROXY_URL`，或优先使用 Semantic Scholar / OpenAlex 替代。

### PubMed 无法下载 PDF
PubMed 是索引数据库，不直接提供 PDF。可以：
- 使用 `download_with_fallback` 通过 DOI 自动查找 OA 全文
- 检查 PMC 是否有免费全文：`python scripts/search.py pmc "PMID:12345678"`

### Semantic Scholar 速率限制
配置 `PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY`；若 key 被拒（403），连接器会自动降级为无 key 模式重试。

### CORE / OpenAIRE 不稳定
CORE 建议配置免费 API Key；OpenAIRE 连接器内置 3 次重试和请求头升级策略，失败时静默返回空结果。

## 推荐下一步

| 触发条件 | 推荐 |
|---------|------|
| 找到论文，需要深度调研 | 使用 `deep-research` — 8 步法深度调研 |
| 需要写学术论文 | 使用 `academic-writing-suite` — 学术写作编排（5 阶段） |
| 需要读论文全文 | 使用 `ai4scholar-integration` — 学术研究工具集成 |

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 与 deep-research 配合时作为第七轮搜索策略
- 搜索结果自动归类为 L1 级别学术资料

### Custom Instruction Injection

学术搜索建议使用英文关键词以获得更好结果

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 多源并发搜索 | 用户请求跨多个数据库搜索时 | 展示将查询的数据库列表，确认搜索范围符合预期 |
| PDF 下载确认 | 找到论文并准备下载时 | 展示论文标题、来源和大小，确认下载目录 |
| API Key 依赖 | 搜索 IEEE/ACM 等需 API Key 的数据库时 | 提示需要配置对应环境变量，确认用户有可用 Key 或切换到开放数据库 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| Google Scholar 反爬限制 | 搜索返回空结果或 429 状态码 | 切换到 Semantic Scholar 或 OpenAlex，或配置代理变量 |
| Semantic Scholar 速率限制 | 返回 429 或大量空结果 | 降级为无 Key 模式重试，或间隔 5s 后再次请求 |
| PDF 下载失败 | fallback 链所有来源均失败 | 提示用户论文可能非开放获取，建议通过机构图书馆或 Sci-Hub 获取 |
| 依赖缺失 | `ModuleNotFoundError: No module named 'xxx'` | 运行 `pip install requests feedparser PyPDF2 scholarly httpx beautifulsoup4` 安装依赖 |