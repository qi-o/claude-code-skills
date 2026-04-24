---
name: sync-all
description: 统一技能同步工作流 - 扫描→更新→验证→同步到GitHub。当用户说"sync-all"、"/sync-all"、"全面同步"时使用。
---

# Sync All

一条命令完成技能生命周期管理：扫描过时→批量更新→二次验证→同步到GitHub。

## 执行流程

按顺序执行以下 5 步，不可跳步。

可选参数（如用户指定，传递给 Step 4）：
- `--skills-only` — Step 4 只同步技能仓库
- `--config-only` — Step 4 只同步配置仓库
- `--dry-run` — Step 4 预览变更，不提交

### Step 1: 扫描过时技能

```bash
python ~/.claude/skills/skill-manager/scripts/scan_and_check.py
```

解析 JSON 输出，提取 `status: "outdated"` 的技能列表。

- 如果扫描脚本报错 → **STOP**，报告错误，不继续
- 如果无过时技能 → 跳到 Step 4

### Step 2: 批量更新

```bash
python ~/.claude/skills/skill-manager/scripts/batch_update.py --auto-update
```

`batch_update.py --auto-update` 会独立扫描所有技能并自动更新检测到的过时技能（内部有自己的扫描逻辑，无需手动传入列表）。

- 如果更新失败 → 报告失败技能名称，继续执行已成功的

### Step 3: 二次验证

```bash
python ~/.claude/skills/skill-manager/scripts/scan_and_check.py
```

确认所有技能状态为 `current`。

- 如果仍有 `outdated` → 报告哪些技能更新失败，但继续 Step 4
- 如果全部 `current` → 正常继续

### Step 4: 同步到 GitHub

```bash
python ~/.claude/skills/sync-to-github/scripts/sync_to_github.py [--skills-only|--config-only] [--dry-run]
```

将 `~/.claude/` 镜像同步到本地 Git 仓库并提交。可选参数由此步骤透传给 `sync_to_github.py`。

- 如果提交失败 → 报告 git 错误详情
- 如果无变更（`[SKIP]`）→ 正常，继续 Step 5

### Step 5: 输出摘要

向用户输出结构化摘要：

```
=== Sync All 完成 ===
扫描: X 个技能, Y 个过时
更新: Z 个成功, W 个失败
验证: 全部 current / 仍有 N 个 outdated
同步: skills [OK/SKIP], config [OK/SKIP]
推送: 请用 GitHub Desktop 推送
```

提示用户用 GitHub Desktop 推送到远程。

## 错误处理

| 步骤失败 | 处理方式 |
|---------|---------|
| Step 1 扫描失败 | STOP，不继续 |
| Step 2 部分更新失败 | 记录失败项，继续 |
| Step 3 验证未通过 | 记录未通过项，继续 |
| Step 4 同步失败 | 报告 git 错误 |


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 新建纯编排型技能时，frontmatter 只保留 name + description，触发词合并进 description 末尾

### Known Fixes & Workarounds
- Codex 审核发现 triggers 字段非标准——应合并到 description 字段中与其他技能保持一致（如 sync-to-github 的写法）
- 可选参数（--skills-only/--config-only/--dry-run）应在 Step 4 命令中显式标注透传路径，不能只在末尾列出
- batch_update.py --auto-update 内部有独立扫描逻辑，无需 Step 1 传入列表——但 SKILL.md 中应明确说明避免读者误解数据流

### Custom Instruction Injection

创建新技能后应经 Codex 或独立 Agent 审核再交付