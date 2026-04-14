---
name: webnovel-snapshot
description: >
  Snapshot management system — 使用 InkOS Craft Snapshot API 管理项目快照。
  Triggers (EN): create snapshot, save snapshot, snapshot management, rollback to version, restore previous version, list snapshots.
  Triggers (CN): 创建快照, 保存快照, 快照管理, 回滚到, 恢复到之前版本, 列出快照, 快照历史。
allowed-tools: Read Write Edit Grep Bash Task
---

# Webnovel Snapshot (InkOS 集成版)

## 功能概述

- 使用 InkOS Craft Snapshot API 管理项目快照
- 快照包含：strand 状态、chapter contract、anti-trope violations、累计 strand 平衡
- 支持创建、列出、回滚操作

## 快照类型

| 类型 | 说明 | 触发场景 |
|-----|------|---------|
| manual | 手动快照 | 用户主动创建 |
| auto_10ch | 自动快照 | 每10章自动创建 |
| volume | 卷快照 | 卷结束时创建 |
| pre_audit | 审核前快照 | 审核前自动创建 |

## 快照存储

- **位置**: `books/{book-id}/story/craft_snapshots/chapter-{N}.json`
- **内容**: CraftSnapshot JSON

```json
{
  "chapter": 15,
  "timestamp": "2026-04-13T12:00:00Z",
  "strandState": { "chapter": 15, "primary": "quest", "weights": {...} },
  "contract": { "chapter": 15, "hookType": "suspense", "openingType": "dialogue", ... },
  "antiTropeViolations": [],
  "strandBalanceCumulative": { "quest": 60, "fire": 25, "constellation": 15 }
}
```

## 使用方式

### 创建快照

InkOS 在每章写作完成后自动保存 craft snapshot。如需手动创建：

读取当前 craft state 并保存：
```bash
# 查看当前状态
inkos status <book-id>

# craft state 位于 books/{book-id}/story/craft_state.md
# 手动保存当前章节的快照（复制 craft_state 到 craft_snapshots/chapter-{N}.json）
```

### 列出快照

```bash
# 列出所有 craft snapshots
ls books/<book-id>/story/craft_snapshots/

# 查看特定章节的快照
cat books/<book-id>/story/craft_snapshots/chapter-15.json
```

### 回滚快照

回滚到指定章节的 craft state：

1. 读取目标快照：`books/{book-id}/story/craft_snapshots/chapter-{N}.json`
2. 恢复 `craft_state.md` 到快照状态
3. **注意**：回滚只恢复 craft state，不删除已写章节

```bash
# 回滚到第10章的 craft state（需确认）
# 1. 读取 snapshot
cat books/<book-id>/story/craft_snapshots/chapter-10.json
# 2. 将 snapshot 内容写回 craft_state.md
# 3. 确认回滚
```

### 清理旧快照

```bash
# 列出快照按时间排序
ls -lt books/<book-id>/story/craft_snapshots/

# 手动删除旧快照
rm books/<book-id>/story/craft_snapshots/chapter-{old}.json
```

## 与写作流程集成

### 自动快照触发点

1. **每章完成后**：InkOS 自动调用 `saveCraftSnapshot()`
2. **审核前**：在 `inkos audit` 前自动创建
3. **每10章**：章节号为 10 的倍数时自动标记

## 验证

```bash
# 检查快照目录存在
test -d books/<book-id>/story/craft_snapshots/

# 列出快照
ls books/<book-id>/story/craft_snapshots/

# 验证最新快照可读
cat books/<book-id>/story/craft_snapshots/chapter-$(inkos status <book-id> | grep currentChapter | awk '{print $2}').json
```

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 回滚到历史快照 | 用户请求回滚到指定章节 | 展示目标快照的章节号和时间戳，明确告知回滚仅恢复 craft state 不删除已写章节 |
| 删除旧快照 | 用户请求清理快照文件 | 列出将被删除的快照列表，确认删除范围 |
| 手动创建快照 | 用户在非标准时机要求创建快照 | 确认当前章节号和保存位置 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| 快照文件损坏 | JSON 解析失败或字段缺失 | 从 `craft_state.md` 重建快照，跳过损坏文件 |
| 目标快照不存在 | 用户指定回滚的章节无对应快照文件 | 列出所有可用快照，请用户选择最近的版本 |
| InkOS 项目状态异常 | `inkos status` 返回错误 | 检查 `inkos.json` 完整性和 `books/` 目录结构 |
| craft_state.md 缺失 | 无法读取当前 craft state | 提示用户检查 InkOS 写作流程是否正常执行过 |

**原则**：不要静默失败——报错时同时提供修复建议。
