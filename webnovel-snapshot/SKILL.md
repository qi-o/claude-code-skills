---
name: webnovel-snapshot
description: >
  Snapshot management system — create, rollback, and manage project snapshots for webnovel writing.
  Triggers (English): create snapshot, save snapshot, snapshot management, rollback to version, restore previous version, list snapshots, view snapshot history.
  Triggers (Chinese): 创建快照, 保存快照, 快照管理, 回滚到, 恢复到之前版本, 列出快照, 查看快照列表, 快照历史。Also triggers automatically every 10 chapters during serial writing.
allowed-tools: Read Write Edit Grep Bash Task
---

# Webnovel Snapshot - 快照管理

## 功能概述

- 创建项目快照（保存 Truth Files、state.json、index.db）
- 列出所有快照
- 回滚到指定快照
- 自动清理旧快照

## 快照类型

| 类型 | 说明 | 触发场景 |
|-----|------|---------|
| manual | 手动快照 | 用户主动创建 |
| auto_10ch | 自动快照 | 每10章自动创建 |
| volume | 卷快照 | 卷结束时创建 |
| pre_audit | 审核前快照 | 审核前自动创建 |

## 环境设置

```bash
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"
export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

## 使用命令

### 创建快照

```bash
# 手动创建快照
python "${SCRIPTS_DIR}/snapshot_manager.py" create \
  --project-root "${PROJECT_ROOT}" \
  --reason "手动创建快照" \
  --type manual

# 创建审核前快照
python "${SCRIPTS_DIR}/snapshot_manager.py" create \
  --project-root "${PROJECT_ROOT}" \
  --reason "审核前备份" \
  --type pre_audit \
  --chapter-range "1-45"
```

### 列出快照

```bash
python "${SCRIPTS_DIR}/snapshot_manager.py" list \
  --project-root "${PROJECT_ROOT}"
```

### 回滚快照

```bash
# 回滚到指定快照（需要确认）
python "${SCRIPTS_DIR}/snapshot_manager.py" rollback \
  --project-root "${PROJECT_ROOT}" \
  --snapshot-id "snap_manual_20260319_120000"

# 回滚（跳过确认）
python "${SCRIPTS_DIR}/snapshot_manager.py" rollback \
  --project-root "${PROJECT_ROOT}" \
  --snapshot-id "snap_manual_20260319_120000" \
  --yes
```

### 清理旧快照

```bash
# 保留最近10个快照
python "${SCRIPTS_DIR}/snapshot_manager.py" clean \
  --project-root "${PROJECT_ROOT}" \
  --keep 10
```

### 删除指定快照

```bash
python "${SCRIPTS_DIR}/snapshot_manager.py" delete \
  --project-root "${PROJECT_ROOT}" \
  --snapshot-id "snap_manual_20260319_120000"
```

## 与写作流程集成

### 审核前自动创建快照

在 Step 3 (审查) 开始前自动创建：

```bash
# 自动创建 pre_audit 快照
python "${SCRIPTS_DIR}/snapshot_manager.py" create \
  --project-root "${PROJECT_ROOT}" \
  --reason "审核前自动快照" \
  --type pre_audit \
  --chapter-range "1-${chapter_num}"
```

### 每10章自动快照

在 Step 5 (Data Agent) 中检查并自动创建：

```bash
# 获取当前章节数
current_chapter=$(python -c "import json; print(json.load(open('${PROJECT_ROOT}/.webnovel/state.json'))['progress']['current_chapter'])")

# 每10章创建快照
if [ $((current_chapter % 10)) -eq 0 ]; then
  python "${SCRIPTS_DIR}/snapshot_manager.py" create \
    --project-root "${PROJECT_ROOT}" \
    --reason "每10章自动快照" \
    --type auto_10ch \
    --chapter-range "1-${current_chapter}"
fi
```

## 快照存储位置

- 快照目录: `.webnovel/snapshots/`
- 快照文件: `.webnovel/snapshots/snap_{type}_{timestamp}.json`
- Index DB 备份: `.webnovel/snapshots/snap_{type}_{timestamp}.index.db`

## 回滚流程

1. 用户执行回滚命令
2. 系统显示快照信息并要求确认
3. 确认后恢复:
   - Truth Files (`.webnovel/truth_files/*.json`)
   - state.json
   - index.db (如存在备份)
4. 回滚完成

## 验证

```bash
# 测试 SnapshotManager
python "${SCRIPTS_DIR}/snapshot_manager.py" --test

# 列出项目快照
python "${SCRIPTS_DIR}/snapshot_manager.py" list \
  --project-root "${PROJECT_ROOT}"
```


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### Known Fixes & Workarounds
- 快照管理器返回的 chapter_range 为字符串如 '1-10'，不是数组，调用者需注意解析
- SnapshotManager.create_snapshot() 返回 (success, message) 元组，不是单个值
- 快照文件命名格式为 {type}_{timestamp}.json，如 auto_10ch_20260319_123045.json