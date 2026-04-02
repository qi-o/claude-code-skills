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
  新增 GLM (Z.AI) LLM provider 支持（OpenAI 兼容 API）
  新增 --skills 生成 repo 级技能文件、--skip-agents-md 保留自定义上下文、Azure OpenAI wiki 支持
  新增 gitnexus serve 桥接模式（Web UI ↔ CLI）、MCP Prompts（detect_impact/generate_map）
  新增 Java/Kotlin 方法引用、重载消歧、接口分派，统一 Web/CLI ingestion pipeline
  新增 C# MethodExtractor 配置支持
  新增 TypeScript/JavaScript MethodExtractor 配置、C/C++ MethodExtractor（纯虚函数检测）
  新增 Web repo landing screen（可选 repo cards）
  对比 deep-research：deep-research 是调研外部知识，gitnexus 是分析本地代码
  Do NOT use for simple file searches (use Grep/Glob instead) or non-code repositories。
github_url: https://github.com/abhigyanpatwari/GitNexus
github_hash: ba5de0bde4069e36460b17b74b54315290bd081e
version: 1.6.0
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

⚠️ **Important Notice:** GitNexus has NO official cryptocurrency, token, or coin. Any token/coin using the GitNexus name on Pump.fun or any other platform is **not affiliated with, endorsed by, or created by** this project or its maintainers. Do not purchase any cryptocurrency claiming association with GitNexus.

<div align="center">

  <a href="https://trendshift.io/repositories/19809" target="_blank">
    <img src="https://trendshift.io/api/badge/repositories/19809" alt="abhigyanpatwari%2FGitNexus | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/>
  </a>

  <h2>Join the official Discord to discuss ideas, issues etc!</h2>

  <a href="https://discord.gg/AAsRVT6fGb">
    <img src="https://img.shields.io/discord/1477255801545429032?color=5865F2&logo=discord&logoColor=white" alt="Discord"/>
  </a>
  <a href="https://www.npmjs.com/package/gitnexus">
    <img src="https://img.shields.io/badge/npm-v2.4.1-blue" alt="npm"/>
  </a>
  <a href="https://opensource.org/licenses/PolyForm-Noncommercial">
    <img src="https://img.shields.io/badge/License-PolyForm%20Noncommercial-blue" alt="License"/>
  </a>

</div>

## Overview

GitNexus is a **client-side code knowledge graph engine** that helps AI agents understand code structure. It indexes local repositories, builds a queryable knowledge graph, and provides MCP tools for:

| Tool | What it does |
|------|-------------|
| `query` | Find code related to a concept — returns execution flows |
| `context` | 360° view of a symbol — callers, callees, processes |
| `impact` | Symbol blast radius — what breaks at depth 1/2/3 |
| `detect_changes` | Git-diff impact — what your changes affect |
| `rename` | Multi-file coordinated rename with confidence scoring |
| `cypher` | Raw graph queries |
| `list_repos` | Discover indexed repositories |

> **Important:** GitNexus analyzes **local code**, not external knowledge. Use `deep-research` for调研外部知识.

## Quick Start

```bash
# First time in a project — index it
npx gitnexus analyze

# Check if index needs refresh
npx gitnexus status
```

Then read `gitnexus://repo/{name}/context` to verify the index loaded.

## Skill Guide

Use the right skill for your task:

| Task | When to use | Skill |
|------|-------------|-------|
| **Index / CLI** | Index a repo, check status, clean, generate wiki | `gitnexus-cli` |
| **Exploring** | Understand architecture, trace execution flows | `gitnexus-exploring` |
| **Debugging** | Trace bugs, find error sources | `gitnexus-debugging` |
| **Impact Analysis** | Blast radius, safety before editing | `gitnexus-impact-analysis` |
| **Refactoring** | Rename, extract, split safely | `gitnexus-refactoring` |
| **PR Review** | Review PR changes, assess merge risk | `gitnexus-pr-review` |
| **Reference** | Tool/schema quick reference | `gitnexus-guide` |

---

# gitnexus-cli

> Use when the user needs to run GitNexus CLI commands like analyze/index a repo, check status, clean the index, generate a wiki, or list indexed repos. Examples: "Index this repo", "Reanalyze the codebase", "Generate a wiki"

All commands work via `npx` — no global install required.

## Commands

| Command | Purpose |
|---------|---------|
| `analyze` | Build or refresh the index |
| `status` | Check index freshness |
| `clean` | Delete the index |
| `wiki` | Generate documentation from the graph |
| `serve` | Bridge mode (Web UI ↔ CLI) |
| `list` | Show all indexed repos |

> **For detailed CLI flags and options, see the [GitNexus CLI documentation](https://github.com/abhigyanpatwari/GitNexus)**

---

# gitnexus-exploring

> Use when the user asks how code works, wants to understand architecture, trace execution flows, or explore unfamiliar parts of the codebase. Examples: "How does X work?", "What calls this function?", "Show me the auth flow"

## Workflow

```
1. READ gitnexus://repos                          → Discover indexed repos
2. READ gitnexus://repo/{name}/context             → Codebase overview, check staleness
3. gitnexus_query({query: "<what you want to understand>"})  → Find related execution flows
4. gitnexus_context({name: "<symbol>"})            → Deep dive on specific symbol
5. READ gitnexus://repo/{name}/process/{name}      → Trace full execution flow
```

> If step 2 says "Index is stale" → run `npx gitnexus analyze` in terminal.

## Checklist

```
- [ ] READ gitnexus://repo/{name}/context
- [ ] gitnexus_query for the concept you want to understand
- [ ] Review returned processes (execution flows)
- [ ] gitnexus_context on key symbols for callers/callees
- [ ] READ process resource for full execution traces
- [ ] Read source files for implementation details
```

## Tools

**gitnexus_query** — find execution flows related to a concept:

```
gitnexus_query({query: "payment processing"})
→ Processes: CheckoutFlow, RefundFlow, WebhookHandler
→ Symbols grouped by flow with file locations
```

**gitnexus_context** — 360-degree view of a symbol:

```
gitnexus_context({name: "validateUser"})
→ Incoming calls: loginHandler, apiMiddleware
→ Outgoing calls: checkToken, getUserById
→ Processes: LoginFlow (step 2/5), TokenRefresh (step 1/3)
```

## Resources

| Resource | What you get |
|----------|-------------|
| `gitnexus://repo/{name}/context` | Stats, staleness warning (~150 tokens) |
| `gitnexus://repo/{name}/clusters` | All functional areas with cohesion scores (~300 tokens) |
| `gitnexus://repo/{name}/cluster/{name}` | Area members with file paths (~500 tokens) |
| `gitnexus://repo/{name}/process/{name}` | Step-by-step execution trace (~200 tokens) |

---

# gitnexus-debugging

> Use when the user is debugging a bug, tracing an error, or asking why something fails. Examples: "Why is X failing?", "Where does this error come from?", "Trace this bug"

## Workflow

```
1. gitnexus_query({query: "<error or symptom>"})     → Find related execution flows
2. gitnexus_context({name: "<suspect>"})              → See callers/callees/processes
3. READ gitnexus://repo/{name}/process/{name}         → Trace execution flow
4. gitnexus_cypher({query: "MATCH path..."})          → Custom traces if needed
```

> If "Index is stale" → run `npx gitnexus analyze` in terminal.

## Checklist

```
- [ ] Understand the symptom (error message, unexpected behavior)
- [ ] gitnexus_query for error text or related code
- [ ] Identify the suspect function from returned processes
- [ ] gitnexus_context to see callers and callees
- [ ] Trace execution flow via process resource if applicable
- [ ] gitnexus_cypher for custom call chain traces if needed
- [ ] Read source files to confirm root cause
```

## Debugging Patterns

| Symptom | GitNexus Approach |
|---------|-------------------|
| Error message | `gitnexus_query` for error text → `context` on throw sites |
| Wrong return value | `context` on the function → trace callees for data flow |
| Intermittent failure | `context` → look for external calls, async deps |
| Performance issue | `context` → find symbols with many callers (hot paths) |
| Recent regression | `detect_changes` to see what your changes affect |

## Tools

**gitnexus_query** — find code related to error:

```
gitnexus_query({query: "payment validation error"})
→ Processes: CheckoutFlow, ErrorHandling
→ Symbols: validatePayment, handlePaymentError, PaymentException
```

**gitnexus_context** — full context for a suspect:

```
gitnexus_context({name: "validatePayment"})
→ Incoming calls: processCheckout, webhookHandler
→ Outgoing calls: verifyCard, fetchRates (external API!)
→ Processes: CheckoutFlow (step 3/7)
```

---

# gitnexus-impact-analysis

> Use when the user wants to know what will break if they change something, or needs safety analysis before editing code. Examples: "Is it safe to change X?", "What depends on this?", "What will break?"

## Workflow

```
1. gitnexus_impact({target: "X", direction: "upstream"})  → What depends on this
2. READ gitnexus://repo/{name}/processes                   → Check affected execution flows
3. gitnexus_detect_changes()                               → Map current git changes to affected flows
4. Assess risk and report to user
```

> If "Index is stale" → run `npx gitnexus analyze` in terminal.

## Checklist

```
- [ ] gitnexus_impact({target, direction: "upstream"}) to find dependents
- [ ] Review d=1 items first (these WILL BREAK)
- [ ] Check high-confidence (>0.8) dependencies
- [ ] READ processes to check affected execution flows
- [ ] gitnexus_detect_changes() for pre-commit check
- [ ] Assess risk level and report to user
```

## Understanding Output

| Depth | Risk Level | Meaning |
|-------|-----------|---------|
| d=1 | **WILL BREAK** | Direct callers/importers |
| d=2 | LIKELY AFFECTED | Indirect dependencies |
| d=3 | MAY NEED TESTING | Transitive effects |

## Risk Assessment

| Affected | Risk |
|----------|------|
| <5 symbols, few processes | LOW |
| 5-15 symbols, 2-5 processes | MEDIUM |
| >15 symbols or many processes | HIGH |
| Critical path (auth, payments) | CRITICAL |

---

# gitnexus-refactoring

> Use when the user wants to rename, extract, split, move, or restructure code safely. Examples: "Rename this function", "Extract this into a module", "Refactor this class", "Move this to a separate file"

## Workflow

```
1. gitnexus_impact({target: "X", direction: "upstream"})  → Map all dependents
2. gitnexus_query({query: "X"})                            → Find execution flows involving X
3. gitnexus_context({name: "X"})                           → See all incoming/outgoing refs
4. Plan update order: interfaces → implementations → callers → tests
```

> If "Index is stale" → run `npx gitnexus analyze` in terminal.

## Checklists

### Rename Symbol

```
- [ ] gitnexus_rename({symbol_name: "oldName", new_name: "newName", dry_run: true}) — preview all edits
- [ ] Review graph edits (high confidence) and ast_search edits (review carefully)
- [ ] If satisfied: gitnexus_rename({..., dry_run: false}) — apply edits
- [ ] gitnexus_detect_changes() — verify only expected files changed
- [ ] Run tests for affected processes
```

### Extract Module

```
- [ ] gitnexus_context({name: target}) — see all incoming/outgoing refs
- [ ] gitnexus_impact({target, direction: "upstream"}) — find all external callers
- [ ] Define new module interface
- [ ] Extract code, update imports
- [ ] gitnexus_detect_changes() — verify affected scope
- [ ] Run tests for affected processes
```

## Tools

**gitnexus_rename** — automated multi-file rename:

```
gitnexus_rename({symbol_name: "validateUser", new_name: "authenticateUser", dry_run: true})
→ 12 edits across 8 files
→ 10 graph edits (high confidence), 2 ast_search edits (review)
→ Changes: [{file_path, edits: [{line, old_text, new_text, confidence}]}]
```

---

# gitnexus-pr-review

> Use when the user wants to review a pull request, understand what a PR changes, assess risk of merging, or check for missing test coverage. Examples: "Review this PR", "What does PR #42 change?", "Is this PR safe to merge?"

## Workflow

```
1. gh pr diff <number>                                    → Get the raw diff
2. gitnexus_detect_changes({scope: "compare", base_ref: "main"})  → Map diff to affected flows
3. For each changed symbol:
   gitnexus_impact({target: "<symbol>", direction: "upstream"})    → Blast radius per change
4. gitnexus_context({name: "<key symbol>"})               → Understand callers/callees
5. READ gitnexus://repo/{name}/processes                   → Check affected execution flows
6. Summarize findings with risk assessment
```

> If "Index is stale" → run `npx gitnexus analyze` in terminal before reviewing.

## Checklist

```
- [ ] Fetch PR diff (gh pr diff or git diff base...head)
- [ ] gitnexus_detect_changes to map changes to affected execution flows
- [ ] gitnexus_impact on each non-trivial changed symbol
- [ ] Review d=1 items (WILL BREAK) — are callers updated?
- [ ] gitnexus_context on key changed symbols to understand full picture
- [ ] Check if affected processes have test coverage
- [ ] Assess overall risk level
- [ ] Write review summary with findings
```

## Risk Assessment

| Signal | Risk |
|--------|------|
| Changes touch <3 symbols, 0-1 processes | LOW |
| Changes touch 3-10 symbols, 2-5 processes | MEDIUM |
| Changes touch >10 symbols or many processes | HIGH |
| Changes touch auth, payments, or data integrity code | CRITICAL |
| d=1 callers exist outside the PR diff | Potential breakage — flag it |

---

# gitnexus-guide

> Use when the user asks about GitNexus itself — available tools, how to query the knowledge graph, MCP resources, graph schema, or workflow reference. Examples: "What GitNexus tools are available?", "How do I use GitNexus?"

## Always Start Here

For any task involving code understanding, debugging, impact analysis, or refactoring:

1. **Read `gitnexus://repo/{name}/context`** — codebase overview + check index freshness
2. **Match your task to a skill above** and follow that skill's workflow
3. **Follow the checklist** for your task type

> If step 1 warns the index is stale, run `npx gitnexus analyze` in the terminal first.

## Skills Quick Reference

| Task | Skill |
|------|-------|
| Understand architecture / "How does X work?" | `gitnexus-exploring` |
| Blast radius / "What breaks if I change X?" | `gitnexus-impact-analysis` |
| Trace bugs / "Why is X failing?" | `gitnexus-debugging` |
| Rename / extract / split / refactor | `gitnexus-refactoring` |
| Tools, resources, schema reference | `gitnexus-guide` (this file) |
| Index, status, clean, wiki CLI commands | `gitnexus-cli` |
| Review PR | `gitnexus-pr-review` |

## Editor Support

| Editor | MCP | Skills | Hooks (auto-augment) | Support |
|--------|-----|--------|----------------------|---------|
| Claude Code | Yes | Yes | Yes (PreToolUse + PostToolUse) | Full |
| Cursor | Yes | Yes | — | MCP + Skills |
| Codex | Yes | Yes | — | MCP + Skills |
| Windsurf | Yes | — | — | MCP |
| OpenCode | Yes | Yes | — | MCP + Skills |

## MCP Prompts

| Prompt | What It Does |
|--------|-------------|
| `detect_impact` | Pre-commit change analysis — scope, affected processes, risk level |
| `generate_map` | Architecture documentation from the knowledge graph with mermaid diagrams |

## Community Integrations

| Project | Author | Description |
|---------|--------|-------------|
| [pi-gitnexus](https://github.com/tintinweb/pi-gitnexus) | @tintinweb | GitNexus plugin for pi — `pi install npm:pi-gitnexus` |
| [gitnexus-stable-ops](https://github.com/ShunsukeHayashi/gitnexus-stable-ops) | @ShunsukeHayashi | Stable ops & deployment workflows (Miyabi ecosystem) |

## Tools Reference

| Tool | What it gives you |
|------|-------------------|
| `query` | Process-grouped code intelligence — execution flows related to a concept |
| `context` | 360-degree symbol view — categorized refs, processes it participates in |
| `impact` | Symbol blast radius — what breaks at depth 1/2/3 with confidence |
| `detect_changes` | Git-diff impact — what do your current changes affect |
| `rename` | Multi-file coordinated rename with confidence-tagged edits |
| `cypher` | Raw graph queries (read `gitnexus://repo/{name}/schema` first) |
| `list_repos` | Discover indexed repos |

> **Multi-repo:** When only one repo is indexed, the `repo` parameter is optional. With multiple repos, specify which one: `query({query: "auth", repo: "my-app"})`.

## Repo-Specific Skills

When you run `gitnexus analyze --skills`, GitNexus detects functional areas of your codebase (via Leiden community detection) and generates a `SKILL.md` for each one under `.claude/skills/generated/`. Each skill describes a module's key files, entry points, execution flows, and cross-area connections. Skills are regenerated on each `--skills` run to stay current.

## Resources Reference

| Resource | Content |
|----------|---------|
| `gitnexus://repo/{name}/context` | Stats, staleness check |
| `gitnexus://repo/{name}/clusters` | All functional areas with cohesion scores |
| `gitnexus://repo/{name}/cluster/{clusterName}` | Area members |
| `gitnexus://repo/{name}/processes` | All execution flows |
| `gitnexus://repo/{name}/process/{processName}` | Step-by-step trace |
| `gitnexus://repo/{name}/schema` | Graph schema for Cypher |

## Graph Schema

**Nodes:** File, Function, Class, Interface, Method, Community, Process
**Edges (via CodeRelation.type):** CALLS, IMPORTS, EXTENDS, IMPLEMENTS, DEFINES, MEMBER_OF, STEP_IN_PROCESS

```cypher
MATCH (caller)-[:CodeRelation {type: 'CALLS'}]->(f:Function {name: "myFunc"})
RETURN caller.name, caller.filePath
```
