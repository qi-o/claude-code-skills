# Claude Code Skills Collection

个人 Claude Code Skills 集合，涵盖学术研究、生物信息学、文档处理、开发工具等多个领域。

## 🎯 核心特色

### 学术研究工作流
完整的学术研究工具链，从文献搜索到论文写作：

- **ai4scholar-integration** - AI4Scholar MCP 集成（36 个学术工具）
  - 论文搜索（arXiv、PubMed、Semantic Scholar、Google Scholar 等）
  - 引用网络分析
  - 作者追踪与 h-index 查询
  - 自动引用标注（IEEE/APA/Vancouver/Nature 格式）
  - AI 科研绘图（智能绘图、文生图、SVG 矢量图）

- **deep-research** - 深度调研方法论（8 步法）
  - 系统化文献调研
  - 事实抽取与证据卡片
  - 框架对比与推导验证
  - 可交付的结构化报告

- **academic-writing-suite** - 学术写作套件
  - 5 阶段工作流：需求分析 → 文献调研 → 提纲设计 → 内容撰写 → 整合输出
  - 整合 deep-research、paper-search、pub-figures

- **paper-search** - 学术论文搜索工具
  - 支持 8 个学术数据库
  - 离线可用，无需 API Key

- **pub-figures** - 出版级科学图表生成
  - 多面板图表（2x2、1x3 等布局）
  - 森林图、热图、散点图
  - 600 DPI 高分辨率输出

### 生物信息学工具
- **biopython** - 序列分析与 BLAST
- **scanpy** + **anndata** - 单细胞 RNA-seq 分析
- **pydeseq2** - 差异表达分析
- **gene-database** - 快速基因查询
- **kegg-database** + **reactome-database** - 通路分析
- **pdb-database** + **alphafold-database** - 蛋白质结构
- **string-database** - 蛋白质互作网络
- **clinvar-database** + **ensembl-database** - 临床变异解读
- **opentargets-database** - 靶点-疾病关联
- **drugbank-database** - 药物信息
- **hmdb-database** - 代谢组学
- **pydicom** - 医学影像（DICOM）
- **clinicaltrials-database** - 临床试验检索
- **bioservices** - 多数据库统一访问

### 文档处理
- **docx** - Word 文档创建与编辑
- **pptx** - PowerPoint 演示文稿处理
- **pdf** - PDF 文档处理
- **xlsx** - Excel 表格处理

### 开发工具
- **gitnexus** - 代码知识图谱引擎
- **crewai-developer** - CrewAI 多代理协作框架
- **react-best-practices** - React/Next.js 性能优化（57 条规则）
- **frontend-design** - 前端设计最佳实践

### 内容创作
- **manga-learning-creator** - 漫画风格学习读本生成
- **baoyu-article-illustrator** - 文章配图生成
- **baoyu-format-markdown** - Markdown 格式化
- **baoyu-compress-image** - 图片压缩优化
- **ai-check-humanizer** - AI 文本检测与人性化改写

### 网络工具
- **ducksearch** - DuckDuckGo 搜索与内容提取
- **aria2-downloader** - 多线程高速下载（16 线程）
- **novel-downloader** - 网络小说下载与合并

### 其他工具
- **notebooklm** - NotebookLM API 集成
- **windows-cleaner** - Windows 磁盘空间分析与清理
- **treatment-plans** - 医疗治疗计划生成（LaTeX/PDF）

## 🚀 快速开始

### 安装

将此仓库克隆到 Claude Code skills 目录：

```bash
git clone https://github.com/qi-o/claude-code-skills.git ~/.claude/skills
```

### 使用示例

#### 学术研究工作流

```markdown
# 1. 搜索论文
使用 ai4scholar MCP 搜索 arXiv 论文：
"帮我搜索关于 CRISPR 在肿瘤免疫治疗中的最新进展"

# 2. 引用网络分析
"分析 AlphaFold 论文的学术影响力，查看引用网络"

# 3. 深度调研
"深度调研 Transformer 架构优化的最新方法"

# 4. 自动引用标注
"给下面这段 Introduction 加上 IEEE 格式的引用：
[粘贴学术文本]"

# 5. 科研绘图
"帮我画一张 CRISPR-Cas9 基因编辑机制图"

# 6. 学术论文写作
"帮我写一篇关于 Transformer 架构优化的论文"
```

#### 生物信息学分析

```markdown
# 单细胞 RNA-seq 分析
"使用 scanpy 分析这个单细胞数据集"

# 差异表达分析
"用 pydeseq2 进行差异表达分析"

# 通路富集分析
"对这些基因进行 KEGG 通路富集分析"
```

#### 文档处理

```markdown
# 创建 Word 文档
"创建一个包含目录和图表的研究报告"

# 生成 PowerPoint
"根据这些数据创建一个演示文稿"
```

## 📚 核心 Skills 详解

### ai4scholar-integration

AI4Scholar MCP 集成指南，提供 36 个学术工具：

**8 大功能类别**：
1. **论文搜索**（9 个工具）- arXiv、PubMed、bioRxiv、medRxiv、Google Scholar、Semantic Scholar
2. **论文详情**（4 个工具）- 批量获取论文元数据
3. **引用与参考文献**（4 个工具）- 引用网络分析
4. **作者信息**（5 个工具）- h-index、论文列表、作者追踪
5. **论文推荐**（2 个工具）- 基于相似度的智能推荐
6. **PDF 下载与全文阅读**（10 个工具）- 支持多个数据库
7. **文献自动标注**（1 个工具）- auto_cite，支持多种引用格式
8. **科研绘图**（1 个工具）- sci_draw，AI 智能绘图

**与现有 Skills 的集成**：
- 与 `deep-research` 集成：作为第七轮搜索策略的增强版本
- 与 `academic-writing-suite` 集成：Phase 2（文献调研）和 Phase 4（内容撰写）
- 与 `pub-figures` 集成：数据图表 + 概念图组合使用

**详细文档**：参见 `ai4scholar-integration/SKILL.md`

### deep-research

深度调研方法论（8 步法），将模糊主题转化为高质量调研报告：

**核心流程**：
1. 问题类型判断
2. 问题拆解与边界界定
3. 资料分层与权威锁定（L1-L4）
4. 事实抽取与证据卡片
5. 建立对比/分析框架
6. 参照物基准对齐
7. 从事实到结论的推导链
8. 用例验证与可交付化处理

**特色功能**：
- 时效敏感性判断（AI/大模型等快速迭代领域）
- 引用网络分析（使用 ai4scholar MCP）
- 作者追踪与智能推荐
- 7 轮搜索策略（包括学术前沿搜索）

### academic-writing-suite

学术写作套件，协调多个 skills 完成学术写作任务：

**5 阶段工作流**：
1. **需求分析** - 明确文档类型、格式要求、图表需求
2. **文献调研** - 收集 40+ 高质量参考文献（使用 ai4scholar + deep-research）
3. **提纲设计** - 设计文档结构，规划图表位置
4. **内容撰写** - 撰写各章节 + 生成图表（auto_cite + sci_draw + pub-figures）
5. **整合输出** - 生成最终可提交文档（.docx / .pdf / .tex）

## 🔧 配置要求

### AI4Scholar MCP

需要配置 API Key：

1. 访问 [ai4scholar.net](https://ai4scholar.net)
2. 注册并获取 API Key（注册赠送 50 积分）
3. 配置到 MCP 服务器（已通过 MCP 方式接入）

**注意**：arXiv、bioRxiv、medRxiv 工具无需 API Key 即可使用。

### 其他工具

大部分 skills 无需额外配置，开箱即用。部分工具可能需要：
- Python 环境（生物信息学工具）
- Node.js 环境（部分文档处理工具）
- 特定 API Keys（如 Gemini API for manga-learning-creator）

## 📖 使用指南

### 触发 Skills

在 Claude Code 中，直接描述你的需求即可自动触发相应的 skill：

```markdown
# 学术搜索
"搜索关于 CRISPR 的论文" → 触发 ai4scholar-integration

# 深度调研
"深度调研 Transformer 架构" → 触发 deep-research

# 学术写作
"写一篇关于 AI 的论文" → 触发 academic-writing-suite

# 文档处理
"创建一个 Word 文档" → 触发 docx

# 下载文件
"下载这个视频" → 触发 aria2-downloader
```

### 工作流推荐

**学术论文写作完整流程**：

```
1. 文献搜索（ai4scholar）
   ↓
2. 深度调研（deep-research）
   ↓
3. 论文写作（academic-writing-suite）
   ↓
4. 自动标注（ai4scholar auto_cite）
   ↓
5. 图表生成（pub-figures + ai4scholar sci_draw）
   ↓
6. 整合输出（docx/pdf）
```

**生物信息学分析流程**：

```
1. 数据预处理（scanpy/biopython）
   ↓
2. 差异分析（pydeseq2）
   ↓
3. 通路分析（kegg-database/reactome-database）
   ↓
4. 可视化（pub-figures）
   ↓
5. 报告生成（academic-writing-suite）
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/qi-o/claude-code-skills
- **AI4Scholar**: https://ai4scholar.net
- **Claude Code**: https://claude.ai/code

## 📝 更新日志

### 2026-03-11
- ✨ 新增 `ai4scholar-integration` skill（36 个学术工具）
- 🔄 更新 `deep-research` skill，集成 ai4scholar MCP
- 🏗️ 重构仓库结构，移除 `.curated/` 层级
- 📚 完善文档和使用指南

### 历史版本
- 持续更新中...

---

**Made with ❤️ for Academic Research & Bioinformatics**
