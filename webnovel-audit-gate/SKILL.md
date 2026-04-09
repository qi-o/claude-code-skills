---
name: webnovel-audit-gate
description: >
  Human-in-the-Loop (HIL) 审核门 - 显示审查结果并处理用户决策。
  触发场景：
  (1) 章节写作完成后自动触发审核门
  (2) 用户手动调用 "audit-gate --show --chapter N"
  (3) 查看/处理审查问题
  Triggers (EN): audit gate, review chapter, check quality, human review, approve chapter,
  quality gate, review results, chapter audit, manual review, HIL gate.
allowed-tools: Read Write Edit Grep Bash Task
---

# webnovel-audit-gate

## 目标

- 显示章节审查结果（时间线、数值、信息边界）
- 判断是否触发 HIL 审核门
- 处理用户决策（跳过/修改/回滚/接受）
- 更新 Truth Files 记录用户决策

## 使用方式

```
# 查看当前章节审核结果
audit-gate --show

# 查看指定章节审核结果
audit-gate --show --chapter 1

# 手动触发审核（跳过自动流程）
audit-gate --trigger --chapter 1

# 处理审核决策
audit-gate --decide --choice skip   # 跳过
audit-gate --decide --choice modify # 修改后重审
audit-gate --decide --choice rollback # 回滚
```

## 触发条件

### 强制触发 (FORCE)
- P1审查失败（任意维度）
- P2审查失败（高风险）
- Anti-AI检测失败
- 任意维度分数 < 70

### 建议触发 (SUGGEST)
- 首章
- 卷末章
- 用户配置

## 交互流程

```
[写作完成] → [自动审查] → [生成审核报告]
                              ↓
                    [是否触发审核门？]
                     ↙          ↘
                   是           否
                    ↓           ↓
           [展示审核界面]  [继续自动流程]
           - 问题列表
           - 用户选择处理方式
           - 确认后更新Truth Files
           - 继续下一阶段
```

## 问题展示格式

```
============================================================
章节 3 审核报告
============================================================

[审核门触发] 类型: FORCE
触发原因:
  - P1审查失败

[维度分数]
  ✓ 时间线精确性: 8.5/10
  ✗ 数值追踪: 6.0/10
  ✓ 信息边界: 9.0/10

[P1问题] 共2项
  1. 🔴 [blocking] 时间矛盾
     位置: 第3段
     详情: 段落中同时出现'上午'和'月亮': 白天看不到月亮
     建议: 请确保时间描述一致

  2. ⚠️ [warning] 数值不一致
     位置: 数值出现处
     详情: 属性'等级': 之前为10, 现在为12
     建议: 请统一数值为10

[建议]
  - 请确保时间描述一致
  - 注意：以下维度分数较低: 数值追踪(6.0)

============================================================

[请选择处理方式]
  1. 跳过 (skip) - 忽略问题，继续自动流程
  2. 修改 (modify) - 修改后重新审查
  3. 回滚 (rollback) - 回滚到上一版本

请输入选项编号 (1-3):
```

## 用户决策处理

| 决策 | 处理逻辑 |
|------|----------|
| skip | 记录决策到 Truth Files，继续自动流程 |
| modify | 暂停流程，返回编辑状态，用户修改后重新审查 |
| rollback | 从备份恢复上一版本，重新审查 |
| accept | 仅在建议触发时可用，记录决策继续流程 |

## 数据流

1. **输入**: `review_gate.p1_auditors.run_p1_review()` 结果
2. **处理**: `hil_gate.trigger.HILGateTrigger.check_trigger()` 判断触发
3. **展示**: `hil_gate.interface.HILInterface.format_report_text()` 格式化
4. **决策**: 用户选择后调用 `hil_gate.interface.run_hil_flow()` 处理
5. **输出**: 更新 Truth Files，继续或暂停流程

## 配置项

可在 `.webnovel/config.json` 中配置:

```json
{
  "audit_gate": {
    "auto_continue": false,
    "always_suggest_gate": false,
    "min_score_threshold": 70
  }
}
```

## 文件位置

- 触发逻辑: `scripts/hil_gate/trigger.py`
- 界面生成: `scripts/hil_gate/interface.py`
- P1审查器: `scripts/review_gate/p1_auditors.py`
- Skill定义: `skills/webnovel-audit-gate/SKILL.md`


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### Known Fixes & Workarounds
- IssueSeverity 必须使用 class IssueSeverity(str, Enum)，不能是普通类，否则与其他模块不兼容
- P2 审查器返回的 risk_level 为字符串 'high'/'medium'/'low'，不是枚举，需注意类型比较
- HILGateTrigger.check_trigger() 接受单个 dict 参数，键为 p1_result, p2_result, anti_ai_result, scores, is_first_chapter, is_volume_end
- FatigueWords 词典中避免重复键，如 '十分' 只应出现一次