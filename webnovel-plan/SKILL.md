---
name: webnovel-plan
description: |
  Builds volume and chapter outlines using InkOS planning pipeline. Inherits creative constraints and prepares writing-ready chapter plans.
  触发场景：
  (1) 用户说"规划章节"、"制作大纲"、"分卷规划"、"生成章节大纲"、"/webnovel-plan"
  (2) 用户想把总纲细化为卷级/章级大纲
  Do NOT use for project initialization (use webnovel-init instead), or writing chapters (use webnovel-write instead).
allowed-tools: Read Write Edit Grep Bash Task
---

# Outline Planning (InkOS 集成版)

## 目标

- 将总纲细化为卷级 + 章级大纲
- 使用 InkOS Planner 自动计算 Strand Weave 和 Chapter Contract
- 产出可直接用于 `/webnovel-write` 的章级规划

## 执行原则

1. 基于初始化产出的总纲和世界观补齐设定基线
2. Strand Weave 和 Contract 由 InkOS Planner 自动计算（确定性算法，不依赖 LLM）
3. 验证步骤检查 InkOS 生成的 ChapterIntent 是否满足约束

## Reference Loading Levels

- L0: 未确认卷范围前不加载参考
- L1: 每步加载必读文件
- L2: 仅在触发条件满足时加载扩展参考

## Workflow

1. Load project data
2. Build setting baseline
3. Select volume and confirm scope
4. Generate volume beat sheet (节拍表)
5. Generate volume timeline (时间线表)
6. Generate volume skeleton (Strand 分布)
7. Generate chapter outlines via InkOS Planner
8. Validate + save

## 1) Load project data

从 InkOS 项目读取：

```bash
# 查看项目状态
inkos status <book-id>

# 读取 Truth Files
# story/story_bible.md    — 世界观
# story/volume_outline.md — 总纲
# story/book_rules.md     — 题材规则 + webnovelCraft 配置
# story/author_intent.md  — 作者意图
# story/craft_state.md    — Craft 状态
```

## 2) Build setting baseline

与原始技能相同：
- 从 `story/story_bible.md` 和 `story/volume_outline.md` 提取设定基线
- 增量补齐设定文件（不清空、不重写）
- 冲突时阻断并等待用户裁决

## 3) Select volume

从 `volume_outline.md` 读取卷划分，让用户选择要规划的卷。

## 4) Generate volume beat sheet

生成节拍表（承诺→危机递增→中段反转→最低谷→大兑现+新钩子）。

写入：`大纲/第{volume_id}卷-节拍表.md`

硬要求：
- 中段反转（必填）
- 危机链至少 3 次递增
- 卷末新钩子必须落到最后一章

## 5) Generate volume timeline

生成时间线表（时间基准、本卷时间跨度、关键倒计时事件）。

写入：`大纲/第{volume_id}卷-时间线.md`

## 6) Generate volume skeleton

基于题材配置和 Strand Weave 规则生成分卷骨架：

### Strand Weave 规划（InkOS 自动计算）

InkOS Planner 的 `computeStrandDirective()` 自动：
- 读取 `craft_state.md` 中的 strand 历史
- 计算累计权重 vs 目标权重
- 选择最 under-represented 的 strand
- 生成 directive 字符串

Strand 比例（默认）：
- **Quest** (主线推进): 55-65%
- **Fire** (情感/关系): 20-30%
- **Constellation** (世界/谜团): 10-20%

### 爽点密度规划

与原始技能相同：
- 常规章节: 1-2 小爽点
- 关键章节: 2-3 爽点（每 5-8 章）
- 高潮章节: 3-4 爽点（每卷至少 1 个）

## 7) Generate chapter outlines via InkOS

### 方式 A：使用 InkOS Planner（推荐）

```bash
# 对每章调用 InkOS Planner 获取 ChapterIntent
inkos plan <book-id>
```

InkOS Planner 自动生成每个章节的 `ChapterIntent`，包含：
- **目标、冲突、钩子议程**（LLM 生成）
- **Strand directive**（确定性算法：选择最 under-represented strand）
- **Chapter Contract**（确定性算法：hookType/openingType/coolPointPattern/emotionalArc 差异化旋转）
- **Beat context**（从大纲中提取当前章节对应的节拍）

### Chapter Contract 自动差异化

InkOS 的 `computeChapterContract()` 自动确保：
- `hookType` 不与最近 N 章重复（N = differentiationWindow，默认 5）
- `openingType` 不与最近 N 章重复
- `coolPointPattern` 不与最近 N 章重复
- `emotionalArc` 不与最近 N 章重复

如无法通过，自动旋转枚举值（最多 10 次尝试）。

### 方式 B：手动生成

按原始技能的章节格式手动生成，然后验证。

章节格式：
```markdown
### 第 {N} 章：{标题}
- 目标: {20字以内}
- 阻力: {20字以内}
- 代价: {20字以内}
- 时间锚点: {具体时间点}
- Strand: {Quest|Fire|Constellation}  ← InkOS 自动计算
- 反派层级: {无/小/中/大}
- 钩子: {类型} - {30字以内}
- Contract: hookType={...}, openingType={...}, coolPoint={...}, emotionalArc={...}  ← InkOS 自动计算
```

## 8) Validate + save

### Validation checks (必须全部通过)

1. **爽点密度** — 每章 ≥1 小爽点，每 5-8 章至少 1 个关键章节
2. **Strand 比例** — Quest 55-65%, Fire 20-30%, Constellation 10-20%
3. **总纲一致性** — 卷核心冲突贯穿，卷末高潮在最后 3-5 章
4. **约束触发频率** — 反套路规则触发合理
5. **完整性** — 每章有目标/阻力/代价/时间锚点/Strand/钩子
6. **时间线一致** — 时间单调递增，倒计时推进正确
7. **设定补全** — 新增角色/势力已回写到设定文件

### Hard fail conditions

- 节拍表或时间线文件为空
- 任一章节缺少必填字段
- 时间回跳未标注
- 倒计时算术冲突
- 与总纲核心冲突矛盾
- 设定集存在未裁决 BLOCKER

## 与 InkOS 集成的优势

| 原始技能 | InkOS 集成 |
|---------|-----------|
| 手动计算 Strand 分配 | Planner 自动计算（确定性） |
| 手动设计 Contract 差异化 | Planner 自动旋转枚举 + 验证 |
| 手动追踪 strand 历史 | craft_state.md 自动记录 |
| Python 脚本状态管理 | InkOS Truth Files 系统 |

---

## 推荐下一步

| 触发条件 | 推荐 |
|---------|------|
| 大纲规划完成 | 使用 `webnovel-write` — 开始写作 |
| 需要调整设定 | 使用 `webnovel-init` — 修改项目 |
