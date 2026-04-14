---
name: webnovel-write
description: |
  Writes webnovel chapters using InkOS full pipeline. 10-agent pipeline with 37+ audit dimensions.
  触发场景：
  (1) 用户说"写章节"、"写正文"、"写下一章"、"/webnovel-write"
  (2) 用户要求生成网文正文内容
  Do NOT use for project initialization (use webnovel-init) or outlining (use webnovel-plan).
allowed-tools: Read Write Edit Grep Bash Task
---

# Chapter Writing (InkOS 集成版)

## 目标

- 使用 InkOS 完整 10-agent 流水线产出可发布章节
- 默认章节字数目标：2000-2500 字
- 保证审查、润色、Truth Files 更新完整闭环

## InkOS 10-Agent Pipeline

`inkos write next <book-id>` 自动执行以下流程：

```
Planner → Composer → Writer → Normalizer → Auditor → Reviser → Analyzer → Validator
```

| Agent | 职责 | Craft 集成 |
|-------|------|-----------|
| **Planner** | 规划 ChapterIntent（目标、冲突、钩子） | 自动计算 Strand directive + Chapter Contract |
| **Composer** | 组装运行时 ContextPackage + RuleStack | 注入 craft context entries |
| **Writer** | 起草章节正文 + Truth Files settlement | 使用 craft prompt sections |
| **Normalizer** | 长度规范化到目标范围 | — |
| **Auditor** | 37+维度审查 | + anti-trope + contract 维度（39维） |
| **Reviser** | 按审查结果修订 | 5种修订模式（spot-fix/polish/rewrite/rework/anti-detect） |
| **Analyzer** | 从最终内容提取事实更新 Truth Files | 更新 craft_state.md |
| **Validator** | 验证 Truth Files 一致性 | — |

## 模式定义

- `/webnovel-write`：完整流水线（推荐）
- `/webnovel-write --fast`：跳过 style adaptation（draft + audit + revise）
- `/webnovel-write --minimal`：仅 draft + 3 基础审查维度

对应 InkOS 命令：
```bash
# 完整流水线
inkos write next <book-id>

# 仅写草稿（无审查/修订）
inkos draft <book-id>

# 仅审查
inkos audit <book-id>

# 仅修订
inkos revise <book-id> --mode polish
```

## 引用加载等级

- L0：未进入对应步骤前不加载参考
- L1：每步仅加载必读文件
- L2：仅在触发条件满足时加载扩展参考

路径约定：
- `references/...` 相对当前 skill 目录

## References（逐文件引用清单）

### 根目录
- `references/step-3-review-gate.md` — 审查调用模板
- `references/polish-guide.md` — Anti-AI 与 No-Poison 规则（参考用，InkOS 内置 AI Tells 分析器）
- `references/writing/typesetting.md` — 排版规则
- `references/style-adapter.md` — 风格转译规则
- `references/style-variants.md` — 开头/钩子/节奏变体

### writing（问题定向加读）
- `references/writing/combat-scenes.md` — 战斗章
- `references/writing/dialogue-writing.md` — 对话问题
- `references/writing/emotion-psychology.md` — 情绪问题
- `references/writing/scene-description.md` — 场景问题
- `references/writing/desire-description.md` — 主角欲望

## 前置检查

写章节前必须满足：

| 检查项 | 通过条件 | 不通过时 |
|--------|---------|---------|
| InkOS 项目存在 | `inkos book list` 显示书籍 | 返回 `webnovel-init` |
| 大纲已有章节 | `inkos status` 显示章节规划 | 返回 `webnovel-plan` |

```bash
# 检查项目状态
inkos status <book-id>
```

## 执行流程

### Step 1：调用 InkOS 写作流水线

```bash
# 完整流水线（推荐）
inkos write next <book-id>
```

InkOS 自动执行所有步骤。以下说明各步骤在 InkOS 中的对应实现：

### 对应关系

| 原始步骤 | InkOS 对应 | 说明 |
|---------|-----------|------|
| Step 0: 预检 | `inkos status` | InkOS PipelineRunner 自动校验 |
| Step 1: Context Agent + Contract v2 | Planner + Composer | InkOS 自动计算 strand + contract |
| Step 2A: 正文起草 | Writer | InkOS Writer 使用 craft prompt sections |
| Step 2B: 风格适配 | Writer (style prompt) | InkOS 内置风格控制 |
| Step 3: 审查 | ContinuityAuditor | 37+维度 + craft 维度 |
| Step 4: 润色 | Reviser | 5种修订模式 |
| Step 5: Data Agent | Writer settlement | InkOS 自动更新 Truth Files |
| Step 5.5: Truth Files | Writer settlement | InkOS 自动更新所有 7+ Truth Files |
| Step 6: Git 备份 | State snapshots | InkOS 内置状态快照 |

### Craft 自动化

当 `webnovelCraft.enabled = true` 时，InkOS 自动：

1. **Planner** 计算：
   - Strand directive（选择最 under-represented strand）
   - Chapter Contract（hookType/openingType/coolPointPattern/emotionalArc 差异化）

2. **Composer** 注入：
   - Strand Weave directive 作为 context entry
   - Chapter Contract 作为 context entry
   - Anti-trope violations 列表作为 context entry

3. **Writer** 使用：
   - 3 个 craft prompt sections（Strand Directive + Contract + Anti-Trope Checklist）

4. **Auditor** 增加：
   - Dimension 38: anti-trope-compliance
   - Dimension 39: contract-compliance

5. **HIL Gate** 检查：
   - FORCE 触发：P1 失败 / anti-AI 失败 / 维度 < 70
   - SUGGEST 触发：首章 / 卷末章

### Step 2：HIL 审核（如触发）

如果 InkOS 返回 `PAUSE_FOR_HIL` 信号：

```bash
# 进入交互式审查
inkos review <book-id>
```

用户决策：
- **skip** — 记录决策，继续
- **modify** — 调用 `inkos revise` 修改后重新审查
- **rollback** — 恢复 craft snapshot
- **accept** — 接受当前质量

### Step 3：验证输出

```bash
# 检查章节已写入
inkos status <book-id>

# 检查审查分数
inkos audit <book-id>

# 检查 craft state 已更新
# story/craft_state.md 应包含新章的 strand + contract + violations
```

## 充分性闸门（必须通过）

1. 章节文件存在且非空
2. ContinuityAuditor 已产出审查分数
3. 全部 `critical` 问题已处理
4. Anti-AI 检测通过
5. Truth Files 已更新
6. Craft state 已更新（strand + contract）

## 失败处理

| 失败类型 | 恢复方式 |
|---------|---------|
| 草稿质量差 | `inkos revise <book-id> --mode rewrite` |
| 审查问题多 | `inkos revise <book-id> --mode polish` |
| 状态损坏 | `inkos write repair-state <book-id>` |
| Craft state 异常 | 使用 `webnovel-snapshot` 回滚 |

## InkOS 审查维度概览

**37 基础维度**（ContinuityAuditor 内置）：
- 角色一致性（OOC）、数值追踪、信息边界、时间线精确性
- 钩子兑现、情感连贯性、场景连续性、对话质量
- 节奏控制、世界观一致性、设定冲突
- ...等

**2 Craft 维度**（webnovelCraft 启用时）：
- Anti-Trope 合规：检查章节是否违反反套路规则
- Contract 合规：检查章节是否满足 Chapter Contract 要求

## 与原始技能的对比

| 方面 | 原始技能 | InkOS 集成 |
|------|---------|-----------|
| 流水线 | 7步独立流程 | 10-agent 自动化流水线 |
| 审查 | 6个审查子代理 | 37+维度 + 2 craft 维度 |
| 上下文 | Python extract_chapter_context.py | InkOS Composer 自动构建 |
| 状态 | state.json + index.db | 7+ Truth Files + craft_state.md |
| Anti-AI | 7层规则 + 200词黑名单 | InkOS AI Tells Analyzer |
| Contract | 手动 Contract v2 | Planner 自动计算 + 差异化验证 |
| 备份 | Git commit | InkOS state snapshots + craft snapshots |

---

## 推荐下一步

| 触发条件 | 推荐 |
|---------|------|
| 章节完成，需要审查 | 使用 `webnovel-audit-gate` |
| 审查通过，继续写 | 使用 `webnovel-continue` |
| 保存进度 | 使用 `webnovel-snapshot` |

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| HIL 审核触发 | InkOS 返回 PAUSE_FOR_HIL 信号（P1 失败/anti-AI 失败/维度 < 70） | 展示具体问题，请用户选择 skip/modify/rollback/accept |
| 草稿重写 | 审查分数极低或 critical 问题数量 >5 | 确认使用 rewrite 模式重写整章，而非仅 polish |
| Craft 快照回滚 | craft state 异常需要回滚到上一个快照 | 确认回滚目标快照，说明将丢失快照之后的 craft 进展 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| InkOS 命令执行失败 | `inkos write next` 返回非零退出码或异常堆栈 | 运行 `inkos write repair-state <book-id>` 修复状态，再重试 |
| 草稿质量不达标 | Auditor 评分低于 70 且存在 P1 级问题 | 使用 `inkos revise --mode rewrite` 重写，或回滚 craft snapshot |
| Truth Files 未更新 | Validator 报告不一致或 craft_state.md 缺少新章记录 | 手动触发 `inkos analyze <book-id>` 补充更新 |
| 状态损坏 | 连续 2 次 `inkos write next` 失败 | 使用 `webnovel-snapshot` 恢复到最近可用快照 |
