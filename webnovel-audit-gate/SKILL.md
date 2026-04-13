---
name: webnovel-audit-gate
description: >
  Human-in-the-Loop (HIL) 审核门 - 使用 InkOS 内置 HIL 系统显示审查结果并处理用户决策。
  触发场景：
  (1) 章节写作完成后自动触发
  (2) 用户手动调用查看审查结果
  (3) 查看/处理审查问题
  Triggers (EN): audit gate, review chapter, check quality, human review, approve chapter, quality gate, HIL gate.
  Triggers (CN): 审核门, 审查章节, 检查质量, 人工审核, 批准章节, 质量门控.
allowed-tools: Read Write Edit Grep Bash Task
---

# webnovel-audit-gate (InkOS 集成版)

## 目标

- 使用 InkOS 内置 HIL 审核系统显示章节审查结果
- 判断是否触发 Human-in-the-Loop 审核
- 处理用户决策（跳过/修改/回滚/接受）

## InkOS HIL 系统概述

InkOS 在章节审查周期中内置了 HIL gate 机制：

**控制信号** (`ChapterReviewCycleControlSignal`)：
- `PROCEED` → 正常流程，无需人工干预
- `PAUSE_FOR_HIL` → 需要人工审核后才能继续
- `HALT` → 不可恢复，停止流水线

## 触发条件

### 强制触发 (FORCE)
- P1 审查维度失败
- Anti-AI 检测回归
- 任意维度分数 < 70

### 建议触发 (SUGGEST)
- 首章（新项目开篇质量关键）
- 卷末章（确保卷末高潮质量）
- Strand weave 偏离目标 > 20%

## 使用方式

### 查看审查结果

```bash
# 查看最新章节的审查结果
inkos audit <book-id>

# 查看指定章节的审查结果
inkos audit <book-id> --chapter 5

# 交互式审查（进入 HIL 流程）
inkos review <book-id>
```

### 处理审核决策

InkOS 的 `inkos review` 命令进入交互式审查模式：

| 决策 | 对应操作 | InkOS 行为 |
|------|---------|-----------|
| skip | 忽略问题，继续 | 记录决策，进入下一章 |
| modify | 修改后重新审查 | `inkos revise <book-id> --mode polish` |
| rollback | 回滚到上一版本 | 恢复 craft snapshot |
| accept | 接受当前质量 | 仅建议触发时可用 |

## 交互流程

```
[inkos write next] → [10-agent pipeline] → [审查完成]
                                                ↓
                                    [HIL gate 评估]
                                     ↙          ↘
                                   FORCE/SUGGEST  PROCEED
                                    ↓              ↓
                           [展示审核界面]    [自动保存，继续]
                           [inkos review]
                                ↓
                           [用户选择处理方式]
                           - skip: 继续
                           - modify: inkos revise
                           - rollback: 恢复快照
                           - accept: 继续
```

## 问题展示格式

```
============================================================
章节 3 审核报告 (InkOS ContinuityAuditor)
============================================================

[HIL 门触发] 类型: FORCE
触发原因:
  - 维度 '数值追踪' 分数 65 < 阈值 70

[审查维度] (37+ 维度)
  ✓ 时间线精确性: 8.5/10
  ✗ 数值追踪: 6.5/10  ← 低于阈值
  ✓ 信息边界: 9.0/10
  ✓ Anti-Trope 合规: 8.0/10
  ✓ Contract 合规: 9.5/10

[问题列表]
  1. 🔴 [blocking] 数值矛盾
     详情: 等级从10变为12，但章节中无修炼/突破描写
     建议: 添加突破描写或保持等级为10

============================================================

[请选择处理方式]
  1. 跳过 (skip) - 记录决策，继续
  2. 修改 (modify) - 调用 inkos revise
  3. 回滚 (rollback) - 恢复上一章快照
```

## 配置

HIL gate 配置在 `book_rules.md` 的 `webnovelCraft.hilGate` 中：

```yaml
webnovelCraft:
  hilGate:
    forceTriggers:
      - p1_failure
      - anti_ai_failure
      - dimension_below_70
    suggestTriggers:
      - first_chapter
      - volume_end
```

## InkOS 审查维度

InkOS 的 ContinuityAuditor 内置 37+ 审查维度，包括：

**基础维度 (1-37)**：
- 角色一致性（OOC 检测）
- 数值追踪（等级、资源）
- 信息边界（角色不应知道的信息）
- 时间线精确性
- 钩子兑现追踪
- 情感连贯性
- 场景连续性
- 等...

**Craft 维度 (38-39, 当 webnovelCraft 启用时)**：
- Anti-Trope 合规（反套路检查）
- Contract 合规（章节合同满足度）

## 推荐下一步

| 触发条件 | 推荐 |
|---------|------|
| 审查通过 | 使用 `webnovel-continue` 续写下一章 |
| 需要保存进度 | 使用 `webnovel-snapshot` 创建快照 |
| 审查发现质量问题 | 使用 `inkos revise <book-id>` 修改 |
