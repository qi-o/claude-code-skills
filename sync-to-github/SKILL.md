---
name: sync-to-github
description: 同步 Claude Code 技能和配置到 GitHub 仓库。当用户说"sync-to-github"、"同步到github"、"同步配置和技能"、"推送到github"、"sync"时使用。自动同步 ~/.claude/skills/ 到 claude-code-skills 仓库，同步配置文件到 claude-code-config 仓库，执行 git commit，最后提示用户使用 GitHub Desktop 推送。 Do NOT use for general git operations or pushing individual project code.
---

# Sync to GitHub

将 `~/.claude/` 下的技能和配置同步到两个 GitHub 仓库并自动提交。

## 执行

运行一条命令完成所有操作：

```bash
python ~/.claude/skills/sync-to-github/scripts/sync_to_github.py
```

可选参数：
- `--skills-only` — 只同步技能仓库
- `--config-only` — 只同步配置仓库
- `--dry-run` — 预览变更，不提交

脚本会自动处理：
1. 验证两个仓库存在
2. 镜像同步文件（跳过 `.git`、`.omc`、`__pycache__`、`node_modules`、`plugins/cache`）
3. 清理 `settings.json` 中的 API token
4. 生成含具体变更列表的 commit message 并提交
5. 输出结果摘要

## 仓库结构

| 仓库 | 源 | 内容 |
|------|-----|------|
| `~/claude-code-skills` | `~/.claude/skills/` | 所有技能 |
| `~/claude-code-config` | `~/.claude/` 下的配置文件和目录 | CLAUDE.md, settings.json, agents/, commands/, hooks/, plugins/, rules/ |

## 推送

脚本只做本地 commit，不 push。完成后提示用户用 GitHub Desktop 推送（git CLI 和 GitHub Desktop 凭证隔离，push 需通过 Desktop）。

## 初始化

如果仓库不存在，先克隆：

```bash
git clone https://github.com/qi-o/claude-code-skills.git ~/claude-code-skills
git clone https://github.com/qi-o/claude-code-config.git ~/claude-code-config
```
