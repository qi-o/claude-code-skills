---
github_url: https://github.com/iswalle/getnote-cli
github_hash: 3af183747bd87692e2b256b07a3d435a2102956e
name: Get笔记
description: >
  Get笔记 - 通过 getnote CLI 保存、搜索、管理个人笔记和知识库。

  **当以下情况时使用此 Skill**：
  (1) 用户要保存内容到笔记：发链接、发图片、说「记一下」「存到笔记」「保存」「收藏」
  (2) 用户要搜索或查看笔记：「搜一下」「找找笔记」「最近存了什么」「看看原文」
  (3) 用户要管理知识库或标签：「加到知识库」「建知识库」「加标签」「删标签」
  (4) 用户要查看博主、直播内容：「博主的笔记」「直播回放」「直播摘要」
  (5) 用户要查看配额：「还能存多少」「用量」「配额」
  (6) 用户要配置 Get笔记：「配置笔记」「连接 Get笔记」
  Triggers (EN): save note, search notes, getnote, personal knowledge base, note-taking,
  bookmark link, save to notes, clip article, note search, tag notes, note quota.
metadata: {"requires": {"getnote": ">=1.0.16"}, "optionalEnv": ["GETNOTE_API_KEY", "GETNOTE_CLIENT_ID", "GETNOTE_API_URL"], "homepage": "https://biji.com"}
---

# Get笔记 Skill (CLI 版)

## 前置条件

- `getnote` CLI 已安装（`npm install -g @getnote/cli`）
- 已认证（`getnote auth status` 显示 Authenticated）

**每次执行笔记操作前先检查认证状态**：
```bash
getnote auth status
```
若返回 "Not authenticated"，引导用户执行：
- OAuth 登录（推荐）：`getnote auth login`
- API Key 登录：`getnote auth login --api-key gk_live_xxx`（client-id 可选）

凭证保存在 `~/.getnote/config.json`。

---

## 指令路由表

| 指令 | 说明 |
|------|------|
| `/note save` 或「记一下」| 保存文本/链接/图片笔记 |
| `/note search` 或「搜一下」| 全局语义搜索 + 知识库语义搜索 |
| `/note list` 或「最近的笔记」| 浏览列表、查看详情、更新、删除 |
| `/note kb` 或「知识库」| 知识库 CRUD + 博主订阅 + 直播订阅 |
| `/note tag` 或「加标签」| 添加/删除标签 |
| `/note quota` 或「配额」| 查看用量配额 |
| `/note config` 或「配置笔记」| 认证配置 |

---

## 自然语言路由

```
包含 URL                    → save（link 模式）
包含图片路径                → save（image 模式）
「记/存/保存/收藏」          → save（text 模式）
「搜/找找/有没有 XX」        → search
「最近/列表/看看/查笔记」    → list
「改/更新/编辑笔记」         → note update
「知识库」相关              → kb
「博主」相关                → kb bloggers
「直播」相关                → kb lives
「标签」相关                → tag
「配额/用量」               → quota
「配置/授权/连接笔记」       → config
```

**决策原则**：优先匹配最具体的意图。有 URL 就是 save，有图片就是 save image，不确定时询问用户。

---

## 全局参数

| 参数 | 说明 |
|------|------|
| `-o, --output json\|table` | 输出格式（默认 table）。程序解析用 `json` |
| `--api-key <key>` | 临时覆盖 API Key（仅本次调用，不保存） |
| `--env prod\|dev` | 切换 API 环境（除非明确要求否则不要修改） |

---

## 命令参考

### 认证管理

```bash
# OAuth 登录（打开浏览器授权）
getnote auth login

# API Key 登录（无需浏览器）
getnote auth login --api-key gk_live_xxx

# 查看认证状态
getnote auth status

# 退出登录
getnote auth logout
```

API Key 获取：https://www.biji.com/settings/developer

### 保存笔记

```bash
# 保存链接（异步，CLI 自动轮询等待完成）
getnote save https://example.com/article --title "好文章" --tag 阅读

# 保存文字（同步）
getnote save "周五前要回复王总的邮件" --tag 待办 --tag 工作

# 保存图片（异步）
getnote save ./screenshot.png --title "设计稿"

# 查看异步任务进度
getnote task <task_id> -o json
# 返回 {"success":true,"data":{"status":"pending|processing|success|failed","note_id":"..."}}
```

`--tag` 可重复使用，如 `--tag 工作 --tag 重要`。
`-o json` 模式下链接/图片保存会静默轮询，直接返回最终笔记 JSON。

### 查看笔记

```bash
# 最近 20 条笔记（默认每页 20 条）
getnote notes

# 自定义数量
getnote notes --limit 50

# 翻页（用最后一条笔记 ID 作为游标）
getnote notes --since-id 1234567890

# 全部笔记（自动翻页）
getnote notes --all

# JSON 输出
getnote notes -o json
# 返回 {"success":true,"data":{"notes":[...],"has_more":true/false}}

# 笔记详情
getnote note <note_id>

# 只取某个字段
getnote note <note_id> --field content
# 可选字段: id, title, content, type, created_at, updated_at, url, excerpt
```

笔记类型：`plain_text` / `img_text` / `link` / `audio` / `meeting` / `local_audio` / `internal_record` / `class_audio` / `recorder_audio` / `recorder_flash_audio`

### 更新 / 删除笔记

```bash
# 更新标题/内容/标签
getnote note update <note_id> --title "新标题"
getnote note update <note_id> --content "新内容"
getnote note update <note_id> --tag "工作,重要"
# ⚠️ --tag 会替换所有现有标签，如需部分修改用 tag add/remove
# ⚠️ --content 仅 plain_text 类型笔记可用

# 删除笔记（移入回收站）
getnote note delete <note_id> -y
```

### 搜索

```bash
# 全局搜索
getnote search "LLM 推理优化"

# 知识库内搜索
getnote search "RAG" --kb <topic_id>

# 限制结果数（最大 10）
getnote search "关键词" --limit 5 -o json
```

结果按语义相关性排序。`NOTE` 类型有 `note_id`，其他类型（FILE/BLOGGER/LIVE 等）`note_id` 为空。
JSON 响应：`{"results":[{"note_id":"...","title":"...","content":"...","created_at":"...","note_type":"..."}]}` — 注意 `results` 在顶层不在 `data` 下。

### 标签

```bash
# 查看笔记标签
getnote tag list <note_id>
# -o json 返回 {"note_id":"...","tags":[{"id":"...","name":"...","type":"..."}]}（无 success 包裹）

# 添加标签
getnote tag add <note_id> 标签名

# 删除标签（可直接用标签名，或用 tag_id 数字）
getnote tag remove <note_id> <标签名或tag_id>
```

标签类型：`ai`（AI 自动）、`manual`（用户添加）、`system`（系统标签，不可删除）
如需一次性替换所有标签，用 `getnote note update --tag "t1,t2"` 更方便。
`tag remove` 现支持直接传标签名（v1.1.1+），也可传 tag_id 数字。

### 知识库

```bash
# 列出自己创建的知识库
getnote kbs
# -o json 返回 {"success":true,"data":{"topics":[{"topic_id":"...","name":"...","description":"...","note_count":N,"created_at":"..."}],"total":N}}

# 列出订阅的知识库（返回格式同 kbs）
getnote kbs-sub [--page 2]

# 查看知识库内的笔记（默认每页 20 条）
getnote kb <topic_id>
getnote kb <topic_id> --limit 50
getnote kb <topic_id> --all
# -o json 返回 {"success":true,"data":{"notes":[...],"has_more":true/false}}

# 创建知识库（每天限 50 个，北京时间 00:00 重置）
getnote kb create "知识库名" --desc "描述"

# 添加/移除笔记（每次最多 20 个 note_id）
getnote kb add <topic_id> <note_id> [note_id...]
getnote kb remove <topic_id> <note_id> [note_id...]
```

### 博主内容

```bash
# 查看知识库的博主列表（获取 follow_id）
getnote kb bloggers <topic_id> [--page 2]

# 博主内容列表（获取 post_id_alias）
getnote kb blogger-contents <topic_id> <follow_id> [--page 2]

# 博主内容详情（含原文 post_media_text）
getnote kb blogger-content <topic_id> <post_id> -o json
```

查询链路：`kb bloggers` → 取 `follow_id` → `kb blogger-contents` → 取 `post_id_alias` → `kb blogger-content` 获取全文。

### 直播回放

```bash
# 知识库的直播列表（仅已 AI 处理的已结束直播）
getnote kb lives <topic_id> [--page 2]

# 直播详情（AI 摘要 post_summary + 完整转录 post_media_text）
getnote kb live <topic_id> <live_id> -o json
```

### 配额

```bash
getnote quota
# -o json 返回 {"success":true,"data":{"read":{"daily":{limit,used,remaining,reset_at},"monthly":{...}},"write":{...},"write_note":{...}}}
```

---

## Agent 约定

### 输出格式
- 向用户展示时用默认 table 格式（不加 `-o json`）
- 需要程序解析结果时加 `-o json`
- 所有 JSON 响应遵循 `{"success":true,"data":{...}}` 结构，**例外**：`search` 的 `results` 在顶层、`tag list` 无 `success` 包裹

### 知识库 ID
- 用 `getnote kbs -o json` 获取 `data.topics[].topic_id`（不是 `id`）
- 订阅知识库（`kbs-sub` 获取的）是只读的，只有自己创建的（`kbs` 获取的）才支持 add/remove

### 标签操作
- `tag remove` 需要 **tag_id**（数字），不是标签名，必须先 `tag list` 获取
- `system` 类型标签不可删除

### Note ID
- 笔记 ID 是 int64，JavaScript 中务必当字符串处理，避免精度丢失

### 安全
- 笔记数据属于隐私，不在群聊中主动展示笔记全文

### 环境变量
| 变量 | 说明 |
|------|------|
| `GETNOTE_API_KEY` | API Key（优先级高于 config 文件） |
| `GETNOTE_CLIENT_ID` | Client ID |
| `GETNOTE_API_URL` | 覆盖 API 地址 |

---

## 错误处理

CLI 通过 exit code 报告错误：`0` 成功，非零失败，错误详情在 stderr。

| 场景 | 处理 |
|------|------|
| Not authenticated / Error: 未授权 / code 10004 | 引导 `getnote auth login` |
| API error 10001 | 鉴权失败，检查 API Key / Client ID 或重新授权 |
| API error 10201 | 非会员，引导开通 |
| API error 10202 | 限流，降低频率 |
| 笔记/知识库不存在 | 确认 ID 正确 |
| 订阅知识库写入失败 | 提示只读，不可操作 |


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 使用 getnote CLI 而非直接调用 API，避免 Windows 终端编码问题
- 向用户展示用 table 格式，程序解析用 -o json
- 笔记 ID 是 int64，JavaScript 中必须当字符串处理

### Known Fixes & Workarounds
- npm 安装 @getnote/cli 后 wrapper 脚本指向 macOS 二进制 (bin/getnote)，Windows 需改为 bin/getnote.exe，修改路径: C:/nvm4w/nodejs/getnote
- 上游 API 未授权错误码实际为 10004 而非旧文档中的 10001
- note update 命令可能返回 30000 服务调用失败，属上游瞬态错误，非 CLI 或技能问题
- search 命令的 JSON 响应中 results 在顶层而非 data 下，与大多数命令不同
- tag list 的 JSON 响应无 success 包裹，直接返回 {note_id, tags}
- v1.1.1 起 tag remove 支持直接传标签名（不再强制需要 tag_id），auth login 的 --client-id 变为可选参数，notes 命令新增 --limit 支持自定义数量

### Custom Instruction Injection

每次执行笔记操作前先运行 getnote auth status 检查认证状态，未认证时引导用户执行 getnote auth login

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 删除笔记 | 执行 note delete 命令 | 确认笔记标题和 ID，提醒删除移入回收站 |
| 替换所有标签 | note update --tag 会覆盖现有标签 | 警告标签将被完全替换而非追加，确认标签列表 |
| 批量操作 >10 条 | 对多个笔记或知识库执行批量操作 | 展示操作列表，确认范围 |
| 保存链接/图片 | 异步任务可能需要较长处理时间 | 告知用户等待时间，确认继续 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| 认证失效 | auth status 返回 Not authenticated 或 code 10004 | 引导用户执行 getnote auth login 重新授权 |
| API 限流 10202 | 返回 error 10202 | 降低请求频率，等待后重试 |
| 异步任务超时 | save 链接/图片后 task 状态长时间为 pending | 使用 task <task_id> 检查状态，超 5 分钟提示用户手动查看 |
| 搜索无结果 | search 返回空列表 | 尝试更宽泛的关键词，或检查知识库范围是否正确 |