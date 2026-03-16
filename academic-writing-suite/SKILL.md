---
name: academic-writing-suite
description: |
  学术写作套件：协调 deep-research、paper-search 和 pub-figures 完成学术写作任务。
  5 阶段工作流：需求分析 → 文献调研 → 提纲设计 → 内容撰写 → 整合输出。
  触发场景：
  (1) 用户需要撰写学术论文、研究报告、基金申请书
  (2) 用户说"写论文"、"写研究报告"、"写基金申请"
  (3) 需要文献调研 + 图表生成 + 文档输出的综合任务
  (4) 学术写作需要专业图表支持
  Do NOT use for quick literature searches (use paper-search instead) or single-section writing tasks.
license: MIT
---

# Academic Writing Suite - 学术写作套件

协调多个 skill 完成学术写作任务的编排系统。

## 概述

本 skill 整合以下能力：
- **deep-research**: 系统化文献调研（8 步法 + 7 轮搜索）
- **paper-search**: 学术数据库搜索（arXiv、PubMed、Semantic Scholar）
- **pub-figures**: 出版级科学图表生成

## 适用场景

| 场景 | 说明 |
|------|------|
| **研究报告** | 需要文献支撑的技术调研报告 |
| **学术论文** | 期刊/会议论文写作 |
| **基金申请** | 研究计划书、项目申请书 |
| **综述文章** | 领域综述、技术白皮书 |
| **学位论文** | 本科/硕士/博士论文章节 |

## 5 阶段工作流

### Phase 1: 需求分析

**目标**：明确写作任务的范围和要求

**执行步骤**：
1. 确定文档类型（论文/报告/申请书）
2. 明确目标期刊/会议/机构的格式要求
3. 确定字数/页数限制
4. 识别需要的图表类型和数量
5. 设定截止日期和里程碑

**输出**：
```markdown
## 写作需求分析

- **文档类型**：[论文/报告/申请书]
- **目标发表**：[期刊名/会议名/机构]
- **格式要求**：[字数/页数/引用格式]
- **图表需求**：
  - [ ] 流程图/方法图
  - [ ] 数据图表（柱状图/折线图/热图）
  - [ ] 结果对比表
- **时间节点**：[截止日期]
```

### Phase 2: 文献调研

**目标**：收集 40+ 高质量参考文献

**执行步骤**：

1. **启动 deep-research 调研**
   - 使用 8 步法进行系统调研
   - 执行 7 轮搜索策略（包括学术前沿搜索）

2. **使用 paper-search 搜索学术数据库**
   ```bash
   # AI/CS 领域
   python ~/.claude/skills/paper-search/scripts/search.py arxiv "<关键词>" --max 20

   # 生物医学领域
   python ~/.claude/skills/paper-search/scripts/search.py pubmed "<关键词>" --max 20

   # 跨领域综合
   python ~/.claude/skills/paper-search/scripts/search.py semantic "<关键词>" --max 20
   ```

3. **文献分类与筛选**
   - L1 级别：核心参考文献（直接支撑论点）
   - L2 级别：背景文献（提供上下文）
   - L3 级别：补充文献（扩展阅读）

**输出**：
- `~/Downloads/research/<topic>/01_资料来源.md`
- 至少 40 篇参考文献，其中 L1 级别 ≥ 15 篇

### Phase 3: 提纲设计

**目标**：设计文档结构，规划图表位置

**执行步骤**：

1. **确定文档结构**
   ```markdown
   # 论文提纲

   ## 1. 引言 (Introduction)
   - 研究背景
   - 问题陈述
   - 研究目标
   - 贡献总结

   ## 2. 相关工作 (Related Work)
   - 领域 A 研究现状
   - 领域 B 研究现状
   - 本文定位

   ## 3. 方法 (Methods)
   - 整体框架 [Figure 1: 方法流程图]
   - 核心算法
   - 实现细节

   ## 4. 实验 (Experiments)
   - 实验设置 [Table 1: 数据集统计]
   - 主要结果 [Figure 2: 性能对比]
   - 消融实验 [Table 2: 消融结果]

   ## 5. 讨论 (Discussion)
   - 结果分析
   - 局限性
   - 未来工作

   ## 6. 结论 (Conclusion)
   ```

2. **规划图表**
   - 标记每个图表的位置
   - 确定图表类型（使用 pub-figures 支持的类型）
   - 准备图表数据

**输出**：
- `outline.md` - 详细提纲
- `figures_plan.md` - 图表规划

### Phase 4: 内容撰写

**目标**：完成各章节内容 + 生成图表

**执行步骤**：

1. **按章节撰写**
   - 从方法/实验章节开始（最具体）
   - 然后写相关工作（需要文献支撑）
   - 最后写引言和结论（需要全局视角）

2. **使用 pub-figures 生成图表**
   ```python
   # 示例：生成多面板图
   import matplotlib.pyplot as plt
   from matplotlib.gridspec import GridSpec

   # 应用出版级默认设置
   plt.rcParams.update({
       'font.family': 'sans-serif',
       'font.sans-serif': ['Arial', 'DejaVu Sans'],
       'savefig.dpi': 600,
   })

   # 创建图表...
   fig.savefig('Figure_1.pdf', bbox_inches='tight')
   ```

3. **引用管理**
   - 使用一致的引用格式
   - 确保每个论点有文献支撑

**输出**：
- 各章节 Markdown 文件
- 高分辨率图表（PDF + PNG）

### Phase 5: 整合输出

**目标**：生成最终可提交文档

**执行步骤**：

1. **整合所有章节**
   - 合并 Markdown 文件
   - 插入图表
   - 生成参考文献列表

2. **格式转换**（根据目标格式）
   ```bash
   # 转换为 Word
   pandoc paper.md -o paper.docx --reference-doc=template.docx

   # 转换为 LaTeX
   pandoc paper.md -o paper.tex

   # 转换为 PDF
   pandoc paper.md -o paper.pdf --pdf-engine=xelatex
   ```

3. **质量检查**
   - [ ] 所有图表清晰可读
   - [ ] 引用格式一致
   - [ ] 无拼写/语法错误
   - [ ] 符合目标格式要求

**输出**：
- 最终文档（.docx / .pdf / .tex）
- 图表文件夹
- 参考文献文件（.bib）

## 工作目录结构

```
~/Downloads/academic-writing/<project>/
├── 00_需求分析.md           # Phase 1 产出
├── 01_文献调研/             # Phase 2 产出
│   ├── 资料来源.md
│   ├── 事实卡片.md
│   └── papers/              # 下载的论文 PDF
├── 02_提纲/                 # Phase 3 产出
│   ├── outline.md
│   └── figures_plan.md
├── 03_草稿/                 # Phase 4 产出
│   ├── 01_introduction.md
│   ├── 02_related_work.md
│   ├── 03_methods.md
│   ├── 04_experiments.md
│   └── 05_conclusion.md
├── 04_图表/                 # Phase 4 产出
│   ├── Figure_1.pdf
│   ├── Figure_1.png
│   └── ...
├── 05_输出/                 # Phase 5 产出
│   ├── paper.md
│   ├── paper.docx
│   └── references.bib
└── FINAL_论文.md            # 最终版本
```

## 快速启动

使用 orchestrator 脚本初始化项目：

```bash
# 初始化项目
python ~/.claude/skills/academic-writing-suite/scripts/orchestrator.py init "研究主题"

# 执行文献搜索
python ~/.claude/skills/academic-writing-suite/scripts/orchestrator.py search "关键词"

# 生成图表
python ~/.claude/skills/academic-writing-suite/scripts/orchestrator.py figures

# 查看项目状态
python ~/.claude/skills/academic-writing-suite/scripts/orchestrator.py status
```

## 与其他 Skill 的关系

```
┌─────────────────────────────────────────────────────────────┐
│                  academic-writing-suite                      │
│                      (编排层)                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│   │deep-research│  │paper-search │  │ pub-figures │        │
│   │  (调研)     │  │  (搜索)     │  │  (图表)     │        │
│   └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│                    ┌─────┴─────┐                           │
│                    │   docx    │                           │
│                    │  (输出)   │                           │
│                    └───────────┘                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 质量检查清单

### 文献调研质量
- [ ] 参考文献数量 ≥ 40 篇
- [ ] L1 级别文献 ≥ 15 篇
- [ ] 包含近 2 年最新研究
- [ ] 覆盖主要研究方向

### 图表质量
- [ ] 分辨率 ≥ 300 DPI
- [ ] 使用色盲友好配色
- [ ] 字体清晰可读
- [ ] 图例完整

### 写作质量
- [ ] 逻辑结构清晰
- [ ] 论点有文献支撑
- [ ] 无抄袭/过度引用
- [ ] 语言流畅准确

## 版本历史

- **v1.0** (2026-01-28): 初始版本
  - 整合 deep-research、paper-search、pub-figures
  - 5 阶段工作流
  - orchestrator 脚本支持

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 项目目录默认创建在 ~/Downloads/academic-writing/ 下
- orchestrator.py 的 init 命令会自动创建 5 阶段子目录

### Known Fixes & Workarounds
- Windows 路径需要使用 Path 对象处理，避免编码问题
- 中文目录名在 Windows 终端显示可能乱码，但实际创建正确

### Custom Instruction Injection

创建新 skill 时，确保 name 字段使用 kebab-case 格式并与文件夹名一致