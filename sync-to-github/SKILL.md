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

### 首次完整初始化

如果 GitHub 上已有仓库，直接克隆：

```bash
git clone https://github.com/qi-o/claude-code-skills.git ~/claude-code-skills
git clone https://github.com/qi-o/claude-code-config.git ~/claude-code-config
```

### 从零创建仓库

如果 GitHub 上还没有仓库，需要先创建并完成首次推送：

```bash
# 1. 在 GitHub 上创建空仓库（不要初始化 README）
gh repo create qi-o/claude-code-skills --private --description "Claude Code skills backup"
gh repo create qi-o/claude-code-config --private --description "Claude Code config backup"

# 2. 本地初始化并关联 remote
mkdir -p ~/claude-code-skills && cd ~/claude-code-skills
git init && git remote add origin https://github.com/qi-o/claude-code-skills.git

mkdir -p ~/claude-code-config && cd ~/claude-code-config
git init && git remote add origin https://github.com/qi-o/claude-code-config.git

# 3. 运行同步脚本完成首次 commit
python ~/.claude/skills/sync-to-github/scripts/sync_to_github.py

# 4. 首次推送（后续用 GitHub Desktop 推送）
cd ~/claude-code-skills && git push -u origin main
cd ~/claude-code-config && git push -u origin main
```

### 验证仓库状态

确认仓库已正确初始化：

```bash
# 检查仓库是否存在（应输出 .git 目录路径）
ls -d ~/claude-code-skills/.git ~/claude-code-config/.git

# 确认 remote 配置正确
git -C ~/claude-code-skills remote -v
git -C ~/claude-code-config remote -v
```

## 排除机制

脚本通过多层机制排除不需要同步的文件和目录。

### 目录级排除

以下目录名在任何层级都会被跳过（匹配路径中的任意组件）：

| 排除项 | 原因 |
|--------|------|
| `.git` | Git 仓库元数据 |
| `.omc` | oh-my-claudecode 运行时状态（会话数据、计划缓存） |
| `.experimental` | 实验性功能目录 |
| `.curated` | 本地策展数据 |
| `.system` | 系统内部目录 |
| `node_modules` | Node.js 依赖（可重建） |
| `__pycache__` / `*.pyc` | Python 编译缓存 |
| `.pytest_cache` | 测试缓存 |
| `tests` | 技能内部测试文件 |
| `env.d` | 环境变量文件（含 API Key） |

### 特定子目录排除

| 路径 | 原因 |
|------|------|
| `plugins/cache/` | 市场插件下载缓存（数千文件，可重新下载） |

### 敏感信息清理

脚本会对同步后的文件进行 secret 清理，匹配以下模式并替换为占位符：

| 模式 | 替换为 |
|------|--------|
| `sk-*`（Anthropic API Key） | `"YOUR_API_KEY_HERE"` |
| `ghp_*`（GitHub Token） | `"YOUR_GITHUB_TOKEN_HERE"` |
| `xox[bors]-*`（Slack Token） | `"YOUR_SLACK_TOKEN_HERE"` |

主要作用于 `settings.json`。清理是单向的：只影响同步目标仓库中的副本，不修改 `~/.claude/` 源文件。

### 嵌套 .git 清理

技能目录中可能包含自带 `.git` 的子目录（如克隆的技能、市场缓存）。脚本会在同步后自动清理目标仓库中所有非根目录的 `.git`，防止 `not a git repository` 错误。

## Dry-run 验证流程

在正式同步前，建议先用 `--dry-run` 预览变更，确认无误后再执行：

```bash
# 预览全部变更
python ~/.claude/skills/sync-to-github/scripts/sync_to_github.py --dry-run

# 仅预览技能仓库变更
python ~/.claude/skills/sync-to-github/scripts/sync_to_github.py --dry-run --skills-only

# 仅预览配置仓库变更
python ~/.claude/skills/sync-to-github/scripts/sync_to_github.py --dry-run --config-only
```

Dry-run 输出前缀为 `would`，表示这是预览而非实际操作：
- `would sync <name>` — 将同步该文件/目录
- `would remove <name>` — 将删除该文件/目录（源中已不存在）

确认预览结果无误后，去掉 `--dry-run` 执行正式同步。

## 同步策略与冲突处理

### 单向镜像覆盖

同步采用**镜像策略**：目标仓库的内容始终与 `~/.claude/` 源保持一致。

- 源中新增的文件/目录 → 复制到目标
- 源中修改的文件 → 覆盖目标中的旧版本
- 源中删除的文件/目录 → 从目标中移除

目标仓库中存在但源中不存在的文件会被删除（`.git` 目录除外）。

### Local vs Remote 冲突

脚本只做本地 commit，不做 push。因此不存在 local vs remote 的自动合并冲突。

冲突只会在你手动 push 时出现（通过 GitHub Desktop 或 git CLI）：

```bash
# 场景：remote 有新提交（比如你在另一台机器上 push 过）
git -C ~/claude-code-skills pull --rebase origin main
```

如果 pull 时出现冲突：

```bash
# 1. 查看冲突文件
git -C ~/claude-code-skills diff --name-only --diff-filter=U

# 2. 方案 A：以本地为准（推荐，因为本地刚从 ~/.claude 同步过）
git -C ~/claude-code-skills checkout --ours .
git -C ~/claude-code-skills add -A
git -C ~/claude-code-skills rebase --continue

# 3. 方案 B：放弃本地改动，以 remote 为准
git -C ~/claude-code-skills rebase --abort
git -C ~/claude-code-skills pull origin main
# 然后重新运行同步脚本
python ~/.claude/skills/sync-to-github/scripts/sync_to_github.py
```

### 多机器协作注意事项

如果多台机器共用同一套技能配置：

1. 每次同步前先 pull 最新 remote 内容
2. 修改 `~/.claude/` 后及时运行同步脚本
3. 尽量避免同时在多台机器上修改同一文件
4. 如果出现分歧，以最新同步的那台机器为准（重新运行脚本覆盖即可）

## 常见错误及解决方案

### 仓库不存在

```
[ERROR] claude-code-skills not found at ~/claude-code-skills
Fix: git clone <your-remote> ~/claude-code-skills
```

**原因**：目标目录下没有 `.git` 子目录。
**解决**：按照上方「首次完整初始化」步骤创建或克隆仓库。

### Git commit 失败

```
[FAIL] claude-code-skills commit failed
```

**可能原因**：
- 用户名/邮箱未配置：运行 `git config --global user.name "your-name"` 和 `git config --global user.email "your@email.com"`
- HEAD detached：运行 `git -C ~/claude-code-skills checkout main`
- 磁盘空间不足

### 推送失败（GitHub Desktop）

- **认证过期**：在 GitHub Desktop 中重新登录 GitHub 账号
- **remote URL 变更**：确认 remote 指向正确的仓库地址
- **网络问题**：检查代理设置，GitHub Desktop 的 proxy 设置在 File > Options > Accounts 中

### 权限错误（Windows）

```
skipped <file> (locked)
removed <name> (partial)
```

**原因**：文件被其他进程占用（如编辑器、Claude Code 进程）。
**解决**：关闭占用文件的程序后重新运行同步脚本。脚本会尝试清理，部分文件可能只被部分删除。

### 敏感信息泄露检查

如果担心 secret 清理遗漏，可以手动检查目标仓库：

```bash
# 检查是否还有 sk- / ghp_ / xox- 开头的 token
grep -rE '(sk-[a-zA-Z0-9_-]{20,}|ghp_[a-zA-Z0-9_-]{36,}|xox[bors]-[a-zA-Z0-9-]+)' ~/claude-code-skills/ ~/claude-code-config/
```

如果发现遗漏，需要将对应模式加入脚本中的 `SECRET_PATTERNS` 列表。

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### Known Fixes & Workarounds
- Windows Git Bash 下 robocopy /MIR 会被当作路径参数，用 cmd /c robocopy 或 PowerShell Copy-Item 替代
- robocopy exit 0 但未拷贝文件时，检查目标目录结构——若已存在同名子目录会导致嵌套而非覆盖，改用 Python shutil.copytree dirs_exist_ok=True
- GitHub token 缺 repo scope 导致 push 失败时，用 GitHub Desktop 推送（其凭证与 git CLI 隔离）
- git reset --hard origin/master 会强制覆盖 working tree——reset 前确认没有 unstaged 变更，reset 后重新执行 Python shutil.copytree 重新拷贝文件
- repo 起源不一致时（本地基于旧仓库，上游已切换 remote），git reset --hard origin/master 重建干净状态比 cherry-pick 更可靠
- GitHub fine-grained PAT 使用 github_pat_ 前缀（非 ghp_），SECRET_PATTERNS 必须同时覆盖 ghp_ 和 github_pat_ 两个前缀，否则会导致 token 泄露到公开仓库
- plugins/cache 等被排除目录若已存在于目标仓库，shutil.copytree 在 Windows 上抛 FileExistsError——sync 前应先清理目标中的被排除目录，或在 mirror_tree 中对 excluded 目录做 skip 而非 copy
- git commit 无变更时返回 exit code 1，脚本不应将此判定为 FAIL——应先 git diff --quiet 检查是否有变更，无变更则输出 SKIP 而非 FAIL