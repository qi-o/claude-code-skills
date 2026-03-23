---
name: gitnexus
description: |
  GitNexus 代码知识图谱引擎 - 客户端知识图谱工具，帮助 AI 代理理解代码结构。
  触发场景：
  (1) 用户需要分析项目代码结构、依赖关系
  (2) 用户需要追踪函数调用链
  (3) 用户需要评估代码修改的影响范围
  (4) 用户需要理解大型代码库的架构
  (5) 用户说"索引项目"、"分析代码"、"查调用链"、"影响分析"
  核心功能：代码索引、知识图谱构建、MCP 工具集成（query/context/impact/rename/cypher）
  对比 deep-research：deep-research 是调研外部知识，gitnexus 是分析本地代码
  Do NOT use for simple file searches (use Grep/Glob instead) or non-code repositories。
github_url: https://github.com/abhigyanpatwari/GitNexus
github_hash: 862fdf91856daf8b1d5df3ff2adc70ddc0de40be
version: 1.6.2
created_at: 2026-02-21T00:00:00Z
platform: github
source: https://github.com/abhigyanpatwari/GitNexus
stars: 850
language: TypeScript
license: PolyForm Noncommercial
allowed-tools: "Bash Read Glob Grep"
metadata:
  category: code-analysis
  tags:
    - code-analysis
    - knowledge-graph
    - mcp
    - code-indexing
    - static-analysis
---

# GitNexus

客户端代码知识图谱引擎，将代码库索引为交互式知识图谱，让 AI 代理永不遗漏代码上下文。

> **官方网站**: https://gitnexus.vercel.app
> **GitHub**: https://github.com/abhigyanpatwari/GitNexus
> **Stars**: 850 | **License**: PolyForm Noncommercial

## 快速开始

### 安装 CLI

```bash
npm install -g gitnexus
```

验证安装：

```bash
gitnexus --version
```

### 索引项目

```bash
# 索引当前目录
gitnexus analyze

# 索引指定目录
gitnexus analyze /path/to/project

# 跳过嵌入生成（加快索引速度）
gitnexus analyze --skip-embeddings

# 强制重建索引
gitnexus analyze --force
```

### 核心命令

```bash
# 配置 MCP（一次性）
gitnexus setup

# 索引仓库（或更新）
gitnexus analyze [path]

# 强制重建索引
gitnexus analyze --force

# 跳过嵌入生成（加快索引）
gitnexus analyze --skip-embeddings

# 生成 AI 代理技能文件（从知识图谱生成）
gitnexus analyze --skills

# 启动 MCP 服务器
gitnexus mcp

# 启动本地 HTTP 服务器（支持多仓库 + Web UI 桥接）
gitnexus serve

# 列出所有已索引仓库
gitnexus list

# 显示索引状态
gitnexus status

# 清理当前仓库索引
gitnexus clean

# 清理所有索引
gitnexus clean --all --force

# 从知识图谱生成文档
gitnexus wiki

# 使用自定义模型生成 wiki
gitnexus wiki --model <model>

# 使用自定义 API 生成 wiki
gitnexus wiki --base-url <url>

# 强制全文重建
gitnexus wiki --force

# 启用嵌入生成（更好的搜索，但速度较慢）
gitnexus analyze --embeddings

# 显示跳过的文件（当解析器不可用时）
gitnexus analyze --verbose
```

> **桥接模式**: `gitnexus serve` 连接 CLI 和 Web UI，Web UI 自动检测本地服务器，可浏览所有 CLI 索引的仓库而无需重新上传或重新索引。

### 启动 MCP 服务器

```bash
# 配置 MCP（生成 .mcp.json）
gitnexus setup

# 启动 MCP 服务器
gitnexus mcp
```

## 核心功能

### 1. 代码索引

- 支持 **10+ 编程语言**: TypeScript, JavaScript, Python, Java, C, C++, **C#**（完整支持）, Go, Rust
- **语言感知符号解析引擎**：3 层解析（精确 FQN → 作用域遍历 → 模糊回退），支持 MRO、构造函数解析、接收者约束解析
- 6 阶段索引管道：结构分析 → AST 解析 → 关系解析 → 聚类 → 流程追踪 → 搜索
- 知识图谱存储在项目 `.gitnexus/` 目录（可移植、gitignore）

### 2. MCP 工具（7 个）

| 工具 | 功能 |
|------|------|
| `list_repos` | 发现所有已索引仓库 |
| `query` | 混合搜索（BM25 + 语义 + RRF） |
| `context` | 360度符号视图（定义、调用者、被调用者、导入） |
| `impact` | 爆炸半径分析（修改影响范围） |
| `detect_changes` | Git 差异影响分析 |
| `rename` | 多文件协调重命名 |
| `cypher` | 原始 Cypher 图查询 |

### 编辑器支持

| 编辑器 | MCP | Skills | Hooks | 支持程度 |
|--------|-----|--------|-------|----------|
| **Claude Code** | ✅ | ✅ | ✅ (PreToolUse + PostToolUse) | **完整** |
| **Cursor** | ✅ | ✅ | — | MCP + Skills |
| **Windsurf** | ✅ | — | — | MCP |
| **OpenCode** | ✅ | ✅ | — | MCP + Skills |

### 3. 多仓库 MCP 架构

采用全局注册表机制，单个 MCP 服务器可服务多个已索引仓库，无需逐项目配置。索引存储在各仓库的 `.gitnexus/` 目录中（便携且被 gitignore）。

### 4. 4 个智能体技能

安装至 `.claude/skills/`：探索（代码导航）、调试（调用链追踪）、影响分析（爆炸半径）、重构（依赖映射）。

### 5. 社区集成

| Agent | 安装命令 | 来源 |
|-------|----------|------|
| pi | `pi install npm:pi-gitnexus` | [pi-gitnexus](https://github.com/tintinweb/pi-gitnexus) |

### 6. MCP Resources

| Resource | 用途 |
|----------|------|
| `gitnexus://repos` | 列出所有已索引仓库 |
| `gitnexus://repo/{name}/context` | 代码库统计和可用工具 |
| `gitnexus://repo/{name}/clusters` | 所有功能聚类及关联分数 |
| `gitnexus://repo/{name}/cluster/{name}` | 聚类成员和详情 |
| `gitnexus://repo/{name}/processes` | 所有执行流程 |
| `gitnexus://repo/{name}/process/{name}` | 完整流程追踪及步骤 |
| `gitnexus://repo/{name}/schema` | 图查询 Cypher schema |

### 7. MCP Prompts

| Prompt | 功能 |
|--------|------|
| `detect_impact` | 提交前变更分析 - 范围、影响流程、风险等级 |
| `generate_map` | 从知识图谱生成架构文档（含 mermaid 图表）

### 5. Web UI

访问 https://gitnexus.vercel.app 使用可视化浏览器。

```bash
# 本地运行
git clone https://github.com/abhigyanpatwari/gitnexus.git
cd gitnexus/gitnexus-web
npm install
npm run dev
```

## 使用示例

### 场景 1: 理解项目结构

```bash
gitnexus analyze
```

然后问 Claude Code：
- "这个项目的入口点在哪里？"
- "主要模块是如何组织的？"

### 场景 2: 追踪调用链

问 Claude Code：
- "UserService.login 被哪些函数调用？"
- "这个 API 端点的完整调用链是什么？"

### 场景 3: 影响分析

问 Claude Code：
- "如果修改 auth.js，会影响哪些文件？"
- "这个 API 的改动会影响哪些消费者？"

### 场景 4: 代码搜索

问 Claude Code：
- "找出所有使用 redis 的地方"
- "哪里定义了 handleRequest 函数？"

## 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                      GitNexus 架构                          │
├─────────────────────────────────────────────────────────────┤
│   代码输入 (Git/ZIP) → 索引管道 (6阶段) → 知识图谱 (KuzuDB)│
│                                              │              │
│         ┌────────────────────────────────────┴────────┐     │
│         ▼                                         ▼        │
│   ┌─────────────┐                           ┌─────────┐   │
│   │  MCP Server │                           │ Web UI  │   │
│   │  (7 tools)  │                           │ (WASM)  │   │
│   └─────────────┘                           └─────────┘   │
│         │                                         │        │
│         ▼                                         ▼        │
│   ┌─────────────┐                           ┌─────────┐   │
│   │ AI 代理     │                           │ 知识图  │   │
│   │ (Claude/    │                           │ 可视化  │   │
│   │  Cursor)    │                           │ + Chat  │   │
│   └─────────────┘                           └─────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 常见问题

### Q: 索引很慢怎么办？

```bash
# 跳过嵌入生成
gitnexus analyze --skip-embeddings
```

### Q: Web UI 内存限制？

Web UI 限制约 5000 文件，大项目请使用 CLI + MCP 模式。

### Q: MCP 配置在哪里？

项目根目录的 `.mcp.json`。

### Q: 与其他工具对比？

| 特性 | GitNexus | Sourcegraph | DeepWiki |
|------|----------|-------------|----------|
| 部署方式 | 客户端本地 | SaaS/自托管 | SaaS |
| 图谱能力 | ✅ 原生 | 需企业版 | 有限 |
| MCP 集成 | ✅ 原生 | ❌ | ❌ |
| Token 效率 | 高（预计算） | 中 | 中 |
| 隐私性 | 完全本地 | 需上传代码 | 需上传代码 |

## 与其他 Skills 的配合

| Skill | 配合场景 |
|-------|----------|
| deep-research | 调研外部技术/方案 |
| omo-skills @explore | 深度代码定位 |
| gitnexus | 分析本地代码结构 |

## 许可证

**PolyForm Noncommercial** - 仅限非商业使用

---

## 版本历史

- **v1.4.0** (2026-03-13): 重大更新 — 语言感知符号解析引擎
  - 新增语言感知符号解析（3 层：精确 FQN → 作用域遍历 → 模糊回退）
  - 新增 MRO（方法解析顺序），支持 5 种语言策略（C++ 最左基类、C#/Java 类优先、Python C3 线性化、Rust 限定语法、默认 BFS）
  - 新增构造函数 & 结构体字面量解析（`new Foo()`、`User{...}`、C# 主构造函数）
  - 新增接收者约束解析（通过 TypeEnv 区分 `user.save()` vs `repo.save()`）
  - 新增继承 & 所有权边（HAS_METHOD、OVERRIDES、Go 结构体嵌入、Swift 扩展继承）
  - 新增可选技能生成：`gitnexus analyze --skills`（从知识图谱生成 AI 代理技能）
  - 新增完整 C# 支持（record/delegate/property/field/event 声明类型）
  - 修复 C/C++ 支持（`.h` → C++ 映射、静态链接导出检测、48 种入口点模式）
  - 修复 Rust 支持（`pub` 可见性检测）
  - 新增 DeepSeek 模型配置
  - 1146 个测试全部通过

- **v1.3.11** (2026-03-08): 安全修复
  - 修复 FTS Cypher 注入漏洞（转义搜索查询中的反斜杠）
  - 新增提交后自动重建索引 hook（`gitnexus analyze` 在 commit/merge 后自动运行）

- **v1.3.10** (2026-03-07): 安全加固 + 双帧 MCP 传输
  - MCP 传输缓冲区上限（10 MB 防 OOM 攻击）
  - 新增双帧 MCP 传输（自动检测 Content-Length vs 换行分隔 JSON）
  - 懒加载 CLI 模块（显著提升 `gitnexus mcp` 启动速度）

- **v1.3.9** (2026-03-06): Bug 修复
  - 修复 CALLS 边 sourceId 与节点 ID 格式对齐问题

- **v1.3.2** (2026-03-11): 功能增量更新
  - 新增 `--embeddings` 参数（启用嵌入生成以改善搜索）
  - 新增 `--verbose` 参数（显示跳过的文件日志）
  - 增强 `wiki` 命令（支持 `--model` 和 `--base-url` 自定义）
  - 更新编辑器支持（Claude Code 新增 PostToolUse hooks）

- **v1.3.1** (2026-02-26): 功能增量更新
  - 新增 OpenCode 编辑器支持、MCP Resources、MCP Prompts、Bridge 模式

- **v1.3.0** (2026-02-21): 初始版本
  - 代码索引和分析、MCP 工具封装、影响分析和调用链追踪

---

*此 Skill 由 github-to-skills 自动生成，支持 skill-manager 更新检查*


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 索引项目时使用 --skip-embeddings 加快速度

### Known Fixes & Workarounds
- Skill 创建后需检查根目录和 .curated/ 目录是否都有副本
- scan_and_check.py 扫描时需要检查正确的目录路径

### Custom Instruction Injection

分析项目时先执行 gitnexus analyze 索引代码库