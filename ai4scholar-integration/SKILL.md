---
name: ai4scholar-integration
description: |
  AI4Scholar MCP 集成指南：学术论文搜索、下载、全文阅读、引用分析、作者查询、自动标注、科研绘图。
  支持 arXiv、PubMed、bioRxiv、medRxiv、Google Scholar、Semantic Scholar 等数据库。
  触发场景：
  (1) 搜索学术论文、下载 PDF、阅读全文
  (2) 查询引用网络、作者信息、论文推荐
  (3) 自动为学术文本添加引用（auto_cite）
  (4) AI 科研绘图（sci_draw）
  (5) 与 deep-research、paper-search、academic-writing-suite 配合使用
license: MIT
version: 1.0.0
metadata:
  category: research-knowledge
---

# AI4Scholar MCP Integration

AI4Scholar 是一个强大的学术研究 MCP 服务器，提供 36 个学术工具，覆盖论文搜索、下载、引用分析、自动标注和科研绘图。

## 核心能力

### 1. 论文搜索（9 个工具）

| 工具 | 平台 | 说明 |
|------|------|------|
| `mcp__ai4scholar__search_semantic` | Semantic Scholar | 语义搜索，支持年份过滤 |
| `mcp__ai4scholar__search_pubmed` | PubMed | 生物医学论文，支持日期范围和排序 |
| `mcp__ai4scholar__search_google_scholar` | Google Scholar | 通过 ai4scholar 代理搜索，支持年份过滤 |
| `mcp__ai4scholar__search_arxiv` | arXiv | 预印本论文搜索 |
| `mcp__ai4scholar__search_biorxiv` | bioRxiv | 生物学预印本 |
| `mcp__ai4scholar__search_medrxiv` | medRxiv | 医学预印本 |
| `mcp__ai4scholar__search_semantic_snippets` | Semantic Scholar | 在论文全文中搜索文本片段 |
| `mcp__ai4scholar__search_semantic_bulk` | Semantic Scholar | 批量搜索（最多 1000 条）|
| `mcp__ai4scholar__search_semantic_paper_match` | Semantic Scholar | 按标题精确匹配 |

### 2. 论文详情（4 个工具）

| 工具 | 说明 |
|------|------|
| `mcp__ai4scholar__get_semantic_paper_detail` | 获取论文详细信息（支持 DOI、arXiv ID、PMID 等）|
| `mcp__ai4scholar__get_pubmed_paper_detail` | 获取 PubMed 论文详情 |
| `mcp__ai4scholar__get_semantic_paper_batch` | 批量获取论文详情（最多 500 篇）|
| `mcp__ai4scholar__get_pubmed_paper_batch` | 批量获取 PubMed 论文详情 |

### 3. 引用与参考文献（4 个工具）

| 工具 | 说明 |
|------|------|
| `mcp__ai4scholar__get_semantic_citations` | 查看谁引用了这篇论文 |
| `mcp__ai4scholar__get_semantic_references` | 查看这篇论文引用了谁 |
| `mcp__ai4scholar__get_pubmed_citations` | PubMed 引用查询 |
| `mcp__ai4scholar__get_pubmed_related` | PubMed 相关论文推荐 |

### 4. 作者信息（5 个工具）

| 工具 | 说明 |
|------|------|
| `mcp__ai4scholar__search_semantic_authors` | 按姓名搜索作者 |
| `mcp__ai4scholar__get_semantic_author_detail` | 获取作者详情（h-index、论文数等）|
| `mcp__ai4scholar__get_semantic_author_papers` | 获取某作者的所有论文 |
| `mcp__ai4scholar__get_semantic_author_batch` | 批量获取作者详情（最多 1000 人）|
| `mcp__ai4scholar__get_semantic_paper_authors` | 获取某论文的所有作者详情 |

### 5. 论文推荐（2 个工具）

| 工具 | 说明 |
|------|------|
| `mcp__ai4scholar__get_semantic_recommendations` | 基于多篇论文推荐相关论文 |
| `mcp__ai4scholar__get_semantic_recommendations_for_paper` | 基于单篇论文推荐 |

### 6. PDF 下载与全文阅读（10 个工具）

| 工具 | 说明 |
|------|------|
| `mcp__ai4scholar__download_semantic` | 获取 Semantic Scholar 开放获取 PDF 链接 |
| `mcp__ai4scholar__read_semantic_paper` | 下载并提取 Semantic Scholar 论文全文 |
| `mcp__ai4scholar__download_arxiv` | 获取 arXiv 论文 PDF 链接 |
| `mcp__ai4scholar__read_arxiv_paper` | 下载并提取 arXiv 论文全文 |
| `mcp__ai4scholar__download_biorxiv` | 获取 bioRxiv 论文 PDF 链接 |
| `mcp__ai4scholar__download_medrxiv` | 获取 medRxiv 论文 PDF 链接 |
| `mcp__ai4scholar__read_biorxiv_paper` | 下载并提取 bioRxiv 论文全文 |
| `mcp__ai4scholar__read_medrxiv_paper` | 下载并提取 medRxiv 论文全文 |
| `mcp__ai4scholar__download_by_doi` | 通过 DOI 下载论文 PDF（支持校园网机构访问）|
| `mcp__ai4scholar__read_by_doi` | 通过 DOI 下载并提取论文全文 |

### 7. 文献自动标注（1 个工具）

| 工具 | 说明 |
|------|------|
| `mcp__ai4scholar__auto_cite` | 一键为学术文本添加真实引用，支持 IEEE/APA/Vancouver/Nature 格式，返回标注文本 + 参考文献列表 + BibTeX |

### 8. 科研绘图（1 个工具）

| 工具 | 说明 |
|------|------|
| `mcp__ai4scholar__sci_draw` | AI 科研绘图：智能绘图（支持中文）、文生图、图片编辑、风格转换、多图组合、迭代优化、图片评审、SVG 矢量图 |

## 与现有 Skills 的集成

### 1. 与 deep-research 集成

在 `deep-research` 的 Step 2（资料分层）中，ai4scholar 作为**第七轮搜索策略**的增强版本：

```markdown
## 第七轮：学术前沿搜索（使用 ai4scholar MCP）

### 优势对比

| 维度 | paper-search skill | ai4scholar MCP |
|------|-------------------|----------------|
| 数据库覆盖 | 8 个 | 6 个（核心相同）|
| 搜索功能 | 基础搜索 | 高级搜索（年份过滤、排序、批量）|
| 引用分析 | ❌ | ✅ 引用网络、参考文献 |
| 作者查询 | ❌ | ✅ 作者详情、h-index、论文列表 |
| 论文推荐 | ❌ | ✅ 基于相似度推荐 |
| 全文阅读 | ✅ | ✅ |
| 自动标注 | ❌ | ✅ auto_cite |
| 科研绘图 | ❌ | ✅ sci_draw |

### 推荐策略

**优先使用 ai4scholar MCP**，因为它提供：
1. **引用网络分析**：追踪论文影响力和学术脉络
2. **作者信息查询**：了解研究团队和学术背景
3. **智能推荐**：发现相关研究
4. **自动标注**：快速生成规范引用

**保留 paper-search skill** 作为备用，用于：
- ai4scholar API 配额不足时
- 需要离线搜索时
```

#### 集成到 deep-research 的具体步骤

在 `deep-research` 的 Step 2 中，添加以下搜索流程：

```markdown
### 第七轮搜索执行流程（ai4scholar 增强版）

1. **基础搜索**（选择合适的数据库）
   ```python
   # AI/机器学习/深度学习
   mcp__ai4scholar__search_arxiv(query="<关键词>", max_results=20)

   # 生物医学/临床
   mcp__ai4scholar__search_pubmed(query="<关键词>", max_results=20, sort="date")

   # 跨领域综合
   mcp__ai4scholar__search_semantic(query="<关键词>", max_results=20, year="2023-")
   ```

2. **引用网络分析**（识别高影响力论文）
   ```python
   # 对搜索结果中的关键论文，查看其引用网络
   mcp__ai4scholar__get_semantic_citations(paper_id="<paper_id>", limit=50)
   mcp__ai4scholar__get_semantic_references(paper_id="<paper_id>", limit=50)
   ```

3. **作者追踪**（识别领域专家）
   ```python
   # 查询高产作者的其他论文
   mcp__ai4scholar__search_semantic_authors(query="<作者名>", limit=5)
   mcp__ai4scholar__get_semantic_author_papers(author_id="<author_id>", limit=20)
   ```

4. **智能推荐**（发现相关研究）
   ```python
   # 基于已找到的核心论文，推荐相关论文
   mcp__ai4scholar__get_semantic_recommendations_for_paper(paper_id="<paper_id>", limit=20)
   ```

5. **全文阅读**（深入理解关键论文）
   ```python
   # 下载并提取论文全文
   mcp__ai4scholar__read_arxiv_paper(paper_id="<arxiv_id>", save_path="./downloads")
   mcp__ai4scholar__read_semantic_paper(paper_id="<paper_id>", save_path="./downloads")
   ```
```

### 2. 与 academic-writing-suite 集成

在 `academic-writing-suite` 的 Phase 2（文献调研）和 Phase 4（内容撰写）中集成 ai4scholar：

#### Phase 2 增强：文献调研

```markdown
### Phase 2: 文献调研（ai4scholar 增强版）

**目标**：收集 40+ 高质量参考文献 + 引用网络分析

**执行步骤**：

1. **基础搜索**（使用 ai4scholar MCP）
   - 搜索核心论文（20-30 篇）
   - 分析引用网络（识别高影响力论文）
   - 追踪领域专家（查询作者论文列表）

2. **智能推荐**
   - 基于核心论文推荐相关研究（10-20 篇）
   - 发现交叉领域研究

3. **全文阅读**
   - 下载关键论文 PDF
   - 提取全文进行深度分析

**输出**：
- `~/Downloads/academic-writing/<project>/01_文献调研/资料来源.md`
- `~/Downloads/academic-writing/<project>/01_文献调研/引用网络.md`（新增）
- `~/Downloads/academic-writing/<project>/01_文献调研/作者分析.md`（新增）
- `~/Downloads/academic-writing/<project>/01_文献调研/papers/`（PDF 文件）
```

#### Phase 4 增强：内容撰写

```markdown
### Phase 4: 内容撰写（ai4scholar 增强版）

**新增功能**：

1. **自动引用标注**（使用 auto_cite）
   ```python
   # 为学术文本自动添加引用
   mcp__ai4scholar__auto_cite(
       text="<学术文本>",
       style="IEEE",  # 或 APA、Vancouver、Nature
       max_results=10
   )
   ```

   **输出**：
   - 标注好的文本（带引用标记）
   - 参考文献列表
   - BibTeX 格式引用

2. **科研绘图**（使用 sci_draw）
   ```python
   # AI 科研绘图
   mcp__ai4scholar__sci_draw(
       prompt="<绘图描述>",
       mode="intelligent",  # 智能绘图
       quality="high"
   )
   ```

   **支持功能**：
   - 智能绘图（支持中文描述）
   - 文生图
   - 图片编辑
   - 风格转换
   - 多图组合
   - SVG 矢量图
```

### 3. 与 pub-figures 集成

ai4scholar 的 `sci_draw` 工具可以作为 `pub-figures` 的补充：

| 维度 | pub-figures | ai4scholar sci_draw |
|------|-------------|---------------------|
| 图表类型 | 数据可视化（柱状图、热图、森林图等）| 概念图、示意图、流程图 |
| 输入方式 | Python 代码 + 数据 | 自然语言描述 |
| 输出格式 | PDF + PNG（600 DPI）| PNG + SVG |
| 适用场景 | 实验结果展示 | 方法说明、概念解释 |
| 定制化 | 高（完全控制）| 中（AI 生成）|

**推荐使用策略**：
- **数据图表**：使用 `pub-figures`（精确控制）
- **概念图/示意图**：使用 `ai4scholar sci_draw`（快速生成）
- **组合使用**：pub-figures 生成数据图 + sci_draw 生成示意图

## 使用示例

### 示例 1：深度文献调研

```markdown
用户：帮我深度调研 CRISPR 在肿瘤免疫治疗中的最新进展

执行流程：
1. 使用 ai4scholar 搜索 PubMed 和 Semantic Scholar
2. 分析高引论文的引用网络
3. 追踪领域专家的最新研究
4. 推荐相关交叉领域研究
5. 下载关键论文全文进行深度分析
6. 使用 deep-research 8 步法整合调研结果
```

### 示例 2：学术论文写作

```markdown
用户：帮我写一篇关于 Transformer 架构优化的论文

执行流程：
1. Phase 1: 需求分析（确定目标会议/期刊）
2. Phase 2: 文献调研
   - 使用 ai4scholar 搜索 arXiv 和 Semantic Scholar
   - 分析引用网络，识别核心论文
   - 追踪领域专家（如 Vaswani 等）
   - 下载 20+ 篇关键论文全文
3. Phase 3: 提纲设计
4. Phase 4: 内容撰写
   - 使用 auto_cite 自动添加引用
   - 使用 sci_draw 生成 Transformer 架构图
   - 使用 pub-figures 生成性能对比图
5. Phase 5: 整合输出
```

### 示例 3：引用网络分析

```markdown
用户：分析 AlphaFold 论文的学术影响力

执行流程：
1. 搜索 AlphaFold 论文（Semantic Scholar）
2. 获取引用该论文的所有论文（citations）
3. 分析引用论文的领域分布
4. 识别高影响力的引用论文
5. 追踪引用作者的研究方向
6. 生成引用网络可视化报告
```

### 示例 4：自动引用标注

```markdown
用户：给下面这段 Introduction 加上引用，用 IEEE 格式

执行流程：
1. 调用 auto_cite 工具
2. 服务端自动匹配相关论文
3. 返回标注好的文本 + 参考文献列表 + BibTeX
4. 用户审核并调整引用
```

### 示例 5：科研绘图

```markdown
用户：帮我画一张 CRISPR-Cas9 基因编辑机制图

执行流程：
1. 调用 sci_draw 工具
2. 使用智能绘图模式（支持中文描述）
3. 生成高质量示意图（PNG + SVG）
4. 如需调整，使用图片编辑功能迭代优化
```

## 工作流集成图

```
┌─────────────────────────────────────────────────────────────┐
│                  学术研究工作流                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │ deep-research│                                           │
│  │  (调研框架)  │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ├─ Step 2: 资料分层                                 │
│         │    │                                               │
│         │    ├─ 第七轮：学术前沿搜索                         │
│         │    │    │                                          │
│         │    │    ├─ ai4scholar MCP（优先）                 │
│         │    │    │   ├─ 论文搜索                           │
│         │    │    │   ├─ 引用分析                           │
│         │    │    │   ├─ 作者追踪                           │
│         │    │    │   ├─ 智能推荐                           │
│         │    │    │   └─ 全文阅读                           │
│         │    │    │                                          │
│         │    │    └─ paper-search skill（备用）             │
│         │    │                                               │
│         │    └─ 其他轮次...                                  │
│         │                                                    │
│         └─ Step 3-8: 事实抽取、框架对比、推导验证...         │
│                                                              │
│  ┌──────────────────────┐                                   │
│  │ academic-writing-suite│                                  │
│  │    (写作编排)         │                                  │
│  └──────┬───────────────┘                                   │
│         │                                                    │
│         ├─ Phase 2: 文献调研                                │
│         │    └─ ai4scholar MCP（搜索 + 引用分析 + 作者追踪）│
│         │                                                    │
│         ├─ Phase 4: 内容撰写                                │
│         │    ├─ auto_cite（自动引用标注）                   │
│         │    ├─ sci_draw（概念图/示意图）                   │
│         │    └─ pub-figures（数据图表）                     │
│         │                                                    │
│         └─ Phase 5: 整合输出                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 配置要求

### MCP 服务器配置

ai4scholar 已通过 MCP 方式接入，配置位于 `~/.claude/mcp_settings.json` 或 Claude Code 配置文件中。

**验证配置**：
```bash
# 检查 MCP 服务器状态
# 在 Claude Code 中，ai4scholar 工具应该自动可用
```

### API Key 配置

ai4scholar 需要 API Key 才能使用完整功能：

1. 访问 [ai4scholar.net](https://ai4scholar.net?src=openclaw)
2. 注册并获取 API Key（注册赠送 50 积分）
3. 配置到 MCP 服务器（已完成）

**注意**：
- arXiv、bioRxiv、medRxiv 工具无需 API Key 即可使用
- 其他工具需要 API Key

## 最佳实践

### 1. 搜索策略

- **关键词选择**：使用英文关键词，组合多个术语
- **时间范围**：对于快速发展的领域，限制在近 2 年
- **数据库选择**：
  - AI/CS → arXiv + Semantic Scholar
  - 生物医学 → PubMed + bioRxiv
  - 跨领域 → Semantic Scholar

### 2. 引用网络分析

- **识别核心论文**：查看被引次数最多的论文
- **追踪研究脉络**：分析引用链条
- **发现新方向**：查看最新引用该论文的研究

### 3. 自动引用标注

- **文本长度**：100-10000 字符
- **引用格式**：根据目标期刊选择（IEEE/APA/Vancouver/Nature）
- **人工审核**：自动标注后需要人工审核和调整

### 4. 科研绘图

- **描述清晰**：提供详细的绘图描述
- **迭代优化**：使用图片编辑功能进行调整
- **格式选择**：PNG 用于预览，SVG 用于最终发表

## 常见问题

### Q: ai4scholar 和 paper-search 有什么区别？

**A**:
- **paper-search**：基础搜索功能，离线可用，无需 API Key
- **ai4scholar**：高级功能（引用分析、作者追踪、自动标注、科研绘图），需要 API Key

**推荐**：优先使用 ai4scholar，paper-search 作为备用

### Q: 如何选择引用格式？

**A**: 根据目标期刊/会议要求：
- **IEEE**：工程/计算机领域
- **APA**：社会科学/心理学
- **Vancouver**：生物医学
- **Nature**：自然科学

### Q: sci_draw 和 pub-figures 如何选择？

**A**:
- **数据图表**（柱状图、热图、散点图）→ pub-figures
- **概念图/示意图**（流程图、架构图、机制图）→ sci_draw
- **组合使用**：数据图 + 示意图

### Q: 如何处理 DOI 下载失败？

**A**:
- 通过 DOI 下载付费论文需要校园网或机构订阅
- 优先使用 `download_semantic`、`download_arxiv` 等开放获取工具
- 如果论文不是开放获取，需要通过机构访问

## 版本历史

- **v1.0** (2026-03-11): 初始版本
  - 整合 ai4scholar MCP 36 个工具
  - 与 deep-research、academic-writing-suite、pub-figures 集成
  - 提供完整使用指南和最佳实践


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- MCP 集成 skill 应包含完整的工具列表（按类别分组）
- 集成指南应明确说明与现有 skills 的关系和优先级
- 提供具体的使用示例和工作流集成图

### Custom Instruction Injection

创建 MCP 集成 skill 时，应包含：1) 工具分类表格 2) 与现有 skills 的对比 3) 工作流集成图 4) 5+ 个使用示例