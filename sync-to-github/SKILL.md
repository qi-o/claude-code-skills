---
name: sync-to-github
description: 同步 Claude Code 技能和配置到 GitHub 仓库。当用户说"sync-to-github"、"同步到github"、"同步配置和技能"、"推送到github"时使用。自动同步 ~/.claude/skills/ 到 claude-code-skills 仓库，同步配置文件到 claude-code-config 仓库，执行 git add 和 commit，最后提示用户使用 GitHub Desktop 推送。 Do NOT use for general git operations or pushing individual project code.
---

# Sync to GitHub

自动同步 Claude Code 的技能和配置文件到对应的 GitHub 仓库。

## 功能

1. **同步技能**: 将 `~/.claude/skills/` 目录同步到 `claude-code-skills` 仓库
2. **同步配置**: 将 Claude Code 配置文件同步到 `claude-code-config` 仓库
3. **自动提交**: 执行 `git add` 和 `git commit`
4. **推送提示**: 完成后提示用户使用 GitHub Desktop 推送

## 工作流程

### 1. 检查仓库

首先检查两个目标仓库是否存在：

```bash
# 检查 claude-code-skills 仓库
test -d ~/claude-code-skills/.git && echo "Skills repo exists" || echo "Skills repo not found"

# 检查 claude-code-config 仓库
test -d ~/claude-code-config/.git && echo "Config repo exists" || echo "Config repo not found"
```

如果仓库不存在，提示用户先克隆仓库。

### 2. 同步技能到 claude-code-skills

使用 `rsync` 同步技能目录，排除不需要的文件：

```bash
rsync -av --delete \
  --exclude='.git' \
  --exclude='.experimental' \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  ~/.claude/skills/ \
  ~/claude-code-skills/
```

**排除规则**:
- `.git`: Git 仓库文件
- `.experimental`: 实验性技能
- `node_modules`, `__pycache__`, `*.pyc`: 依赖和缓存文件

### 3. 同步配置到 claude-code-config

同步以下配置文件和目录：

```bash
# 同步根目录文件
cp ~/.claude/CLAUDE.md ~/claude-code-config/
cp ~/.claude/settings.json ~/claude-code-config/

# 同步目录
rsync -av --delete ~/.claude/agents/ ~/claude-code-config/agents/
rsync -av --delete ~/.claude/commands/ ~/claude-code-config/commands/
rsync -av --delete ~/.claude/hooks/ ~/claude-code-config/hooks/
rsync -av --delete ~/.claude/plugins/ ~/claude-code-config/plugins/
rsync -av --delete ~/.claude/rules/ ~/claude-code-config/rules/
```

**注意**:
- 使用 `--delete` 确保目标目录与源目录完全同步
- `settings.json` 中的敏感信息（API token）应在提交前替换为占位符

### 4. 清理敏感信息

在提交前，自动清理 `settings.json` 中的敏感信息：

```bash
# 使用 sed 替换 API token
sed -i 's/"ANTHROPIC_AUTH_TOKEN": "sk-[^"]*"/"ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY_HERE"/g' \
  ~/claude-code-config/settings.json
```

### 5. 提交更改

为每个仓库生成有意义的 commit message 并提交：

```bash
# 提交技能仓库
cd ~/claude-code-skills
git add -A
git commit -m "$(cat <<'EOF'
同步技能更新

- 更新现有技能
- 添加新技能（如有）
- 删除已移除的技能
EOF
)"

# 提交配置仓库
cd ~/claude-code-config
git add -A
git commit -m "$(cat <<'EOF'
同步配置更新

- 更新 CLAUDE.md 和 settings.json
- 同步 agents, commands, hooks, plugins, rules
- 清理敏感信息
EOF
)"
```

### 6. 推送提示

完成后，输出清晰的提示信息：

```
✅ 同步完成！

📦 已提交的仓库：
  - claude-code-skills: 1 个新提交
  - claude-code-config: 1 个新提交

🚀 下一步：使用 GitHub Desktop 推送
  1. 打开 GitHub Desktop
  2. 选择 claude-code-skills 仓库
  3. 点击 "Push origin" 推送提交
  4. 选择 claude-code-config 仓库
  5. 点击 "Push origin" 推送提交

💡 提示：如果 GitHub Desktop 中看不到 "Push origin" 按钮，
       请检查是否已经选择了正确的仓库。
```

## 错误处理

### 仓库不存在

如果目标仓库不存在，提示用户克隆：

```bash
# 克隆技能仓库
git clone https://github.com/qi-o/claude-code-skills.git ~/claude-code-skills

# 克隆配置仓库
git clone https://github.com/qi-o/claude-code-config.git ~/claude-code-config
```

### 无更改可提交

如果没有更改，跳过提交并通知用户：

```
ℹ️  没有检测到更改，跳过提交。
```

### Git 冲突

如果存在未提交的更改或冲突，提示用户先解决：

```
⚠️  检测到未提交的更改或冲突，请先解决后再同步。
```

## 使用示例

**触发方式**:
- "sync-to-github"
- "同步到github"
- "同步配置和技能"
- "推送到github"

**执行流程**:
1. 检查仓库存在性
2. 同步技能目录
3. 同步配置文件
4. 清理敏感信息
5. 提交更改
6. 显示推送提示

## 最佳实践

1. **定期同步**: 建议在完成重要更改后立即同步
2. **检查差异**: 提交前使用 `git diff` 检查更改
3. **敏感信息**: 确保 API token 等敏感信息已被清理
4. **测试验证**: 推送后在 GitHub 上验证文件是否正确同步


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### Known Fixes & Workarounds
- Windows Git Bash 下 robocopy /MIR 会被当作路径参数，用 cmd /c robocopy 或 PowerShell Copy-Item 替代
- robocopy exit 0 但未拷贝文件时，检查目标目录结构——若已存在同名子目录会导致嵌套而非覆盖，改用 Python shutil.copytree dirs_exist_ok=True
- GitHub token 缺 repo scope 导致 push 失败时，用 GitHub Desktop 推送（其凭证与 git CLI 隔离）
- git reset --hard origin/master 会强制覆盖 working tree——reset 前确认没有 unstaged 变更，reset 后重新执行 Python shutil.copytree 重新拷贝文件
- repo 起源不一致时（本地基于旧仓库，上游已切换 remote），git reset --hard origin/master 重建干净状态比 cherry-pick 更可靠