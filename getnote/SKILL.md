---
name: getnote
description: |
  Get笔记 - 个人笔记和知识库管理工具。

  当用户提到以下意图时使用此技能：
  「记一下」「存到笔记」「保存到Get笔记」「记录到Get笔记」
  「保存这个链接」「保存这张图」「查我的笔记」「找一下笔记」
  「加标签」「删标签」「删笔记」
  「查知识库」「建知识库」「把笔记加到知识库」「从知识库移除」
  「知识库里订阅了哪些博主」「博主发了什么内容」「直播总结」「直播原文」
  「搜一下」「找找我哪些笔记提到了 XX」「在我的 XX 知识库搜一下 XX」

  支持：纯文本笔记、链接笔记（自动抓取网页内容并生成摘要）、图片笔记（OCR识别）、知识库管理（含博主订阅列表、直播总结）、语义搜索召回（全局或指定知识库范围）。

  **注意**：此技能需要配置 Get笔记 API 凭证。
license: MIT-0
github_url: https://github.com/iswalle/getnote-openclaw
github_hash: 7f3f8d5a88d5fb685a27da63078af2b928302787
version: 1.3.2
source: skills/getnote
metadata:
  category: productivity
---

# Get笔记 API

## 快速决策

Base URL: `https://openapi.biji.com`

| 用户意图 | 接口 | 关键点 |
|---------|------|--------|
| 「记一下」「保存笔记」 | POST /open/api/v1/resource/note/save | 同步返回 |
| 「保存这个链接」 | POST /open/api/v1/resource/note/save | note_type:"link" → **必须轮询** |
| 「保存这张图」 | 见「图片笔记流程」 | **4 步流程，必须轮询** |
| 「查我的笔记」 | GET /open/api/v1/resource/note/list | since_id=0 起始 |
| 「看原文/转写内容」 | GET /open/api/v1/resource/note/detail | audio.original / web_page.content |
| 「加标签」 | POST /open/api/v1/resource/note/tags/add | |
| 「删标签」 | POST /open/api/v1/resource/note/tags/delete | system 类型不可删 |
| 「删笔记」 | POST /open/api/v1/resource/note/delete | 移入回收站 |
| 「查知识库」 | GET /open/api/v1/resource/knowledge/list | 含统计数据 |
| 「建知识库」 | POST /open/api/v1/resource/knowledge/create | 每天限 50 个 |
| 「笔记加入知识库」 | POST /open/api/v1/resource/knowledge/note/batch-add | 每批最多 20 条 |
| 「从知识库移除」 | POST /open/api/v1/resource/knowledge/note/remove | |
| 「查任务进度」 | POST /open/api/v1/resource/note/task/progress | 链接/图片笔记轮询用 |
| 「订阅了哪些博主」 | GET /open/api/v1/resource/knowledge/bloggers | 按 topic_id 查 |
| 「博主发了什么内容」 | GET /open/api/v1/resource/knowledge/blogger/contents | 需要 follow_id |
| 「博主内容原文/详情」 | GET /open/api/v1/resource/knowledge/blogger/content/detail | 需要 post_id |
| 「有哪些已完成直播」 | GET /open/api/v1/resource/knowledge/lives | 按 topic_id 查 |
| 「直播总结/直播原文」 | GET /open/api/v1/resource/knowledge/live/detail | 需要 live_id |
| 「搜一下」「找找笔记里提到 XX 的」 | POST /open/api/v1/resource/recall | 全局语义召回 |
| 「在 XX 知识库搜 XX」 | POST /open/api/v1/resource/recall/knowledge | 知识库语义召回 |

---

## 配置

### 环境变量

在 Claude Code 设置中添加以下环境变量：

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `GETNOTE_API_KEY` | ✅ | API Key，格式：`gk_live_xxx` |
| `GETNOTE_CLIENT_ID` | ✅ | Client ID，格式：`cli_xxx` |
| `GETNOTE_OWNER_ID` | ❌ | 用户 ID，用于权限控制 |

**获取凭证**：前往 [Get笔记开放平台](https://www.biji.com/openapi) 创建应用获取。

### 认证

请求头：
- `Authorization: $GETNOTE_API_KEY`（格式：`gk_live_xxx`）
- `X-Client-ID: $GETNOTE_CLIENT_ID`（格式：`cli_xxx`）

### Scope 权限

| Scope | 说明 |
|-------|------|
| note.content.read | 笔记列表、内容读取 |
| note.content.write | 文字/链接/图片笔记写入 |
| note.tag.write | 添加、删除笔记标签 |
| note.content.trash | 笔记移入回收站 |
| topic.read | 知识库列表 |
| topic.write | 创建知识库 |
| note.topic.read | 笔记所属知识库查询 |
| note.topic.write | 笔记加入/移出知识库 |
| note.image.upload | 获取上传图片签名 |
| topic.blogger.read | 读取知识库订阅博主列表和博主内容 |
| topic.live.read | 读取知识库已完成直播列表和直播详情 |
| note.recall.read | 语义召回笔记（全局） |
| note.topic.recall.read | 语义召回知识库内容 |

---

## ⚠️ 必读约束

### 🔤 中文编码处理（重要！）

**必须使用 Python requests 库发送请求**，不要使用 curl。

curl 在 Windows 终端会有编码问题，导致中文变成乱码。

**正确方式 - Python requests：**
```python
import requests
import os

API_KEY = os.environ.get("GETNOTE_API_KEY")
CLIENT_ID = os.environ.get("GETNOTE_CLIENT_ID")

headers = {
    "Authorization": API_KEY,
    "X-Client-ID": CLIENT_ID
}

# 保存笔记
requests.post(
    "https://openapi.biji.com/open/api/v1/resource/note/save",
    headers=headers,
    json={"content": "中文内容", "note_type": "plain_text", "title": "标题"}
)

# 查询笔记
requests.get(
    "https://openapi.biji.com/open/api/v1/resource/note/detail?id=123",
    headers=headers
)
```

**错误方式 - curl：**
```bash
# ❌ 会导致中文乱码
curl -X POST "https://openapi.biji.com/open/api/v1/resource/note/save" \
  -H "Authorization: $GETNOTE_API_KEY" \
  -d '{"content": "中文"}'
```

### 🔢 笔记 ID 处理规则

笔记 ID（`id`、`note_id`、`next_cursor` 等）是 **64 位整数（int64）**，超出 JavaScript `Number.MAX_SAFE_INTEGER`（2^53-1）范围。

### ⚠️ API 参数类型不一致（重要！）

Get笔记 API 有一个奇怪的设计：**不同接口对 ID 类型的要求不同**：

| 接口 | 参数 | 类型要求 |
|------|------|---------|
| POST /note/tags/add | note_id | **整数** (int) |
| POST /note/tags/delete | note_id | 整数 (int) |
| POST /note/tags/delete | tag_id | **字符串** (string) |
| POST /knowledge/note/batch-add | note_ids | 整数/字符串均可 |
| GET /note/detail | id | 字符串/整数均可 |

**错误示例：**
```python
# ❌ note_id 传字符串 - 添加标签失败
requests.post(url, json={"note_id": "123456789", "tags": ["测试"]})

# ❌ tag_id 传整数 - 删除标签失败
requests.post(url, json={"note_id": 123456789, "tag_id": 12345})
```

**正确示例：**
```python
# ✅ 添加标签 - note_id 用整数
requests.post(url, json={"note_id": 123456789, "tags": ["测试"]})

# ✅ 删除标签 - tag_id 用字符串
requests.post(url, json={"note_id": 123456789, "tag_id": "12345"})
```

> 注意：Python 的 JSON 序列化会保留原始类型，只要不从字符串转换就没问题。

**正确做法**：
- **始终把 ID 当字符串处理**，不要做数值运算
- **发请求时**：`note_id` 字段传字符串或数字均可，服务端兼容两种格式

---

### 🔒 安全规则

- 笔记数据属于用户隐私，不在群聊中主动展示笔记内容
- 若配置了 `GETNOTE_OWNER_ID`，检查 sender_id 是否匹配；不匹配时回复「抱歉，笔记是私密的，我无法操作」
- API 返回 `error.reason: "not_member"` 或错误码 `10201` 时，引导开通会员：https://www.biji.com/checkout?product_alias=6AydVpYeKl
- 创建笔记建议间隔 1 分钟以上，避免触发限流

---

## 核心功能

### 笔记列表

```
GET /open/api/v1/resource/note/list?since_id=0
```

- since_id (int64, 必填) - 游标，首次传 0，后续用 next_cursor
- 返回：notes[], has_more, next_cursor, total（每次固定 20 条）

### 笔记详情

```
GET /open/api/v1/resource/note/detail?id={note_id}
```

### 新建笔记

```
POST /open/api/v1/resource/note/save
Content-Type: application/json
```

```json
{
  "title": "笔记标题",
  "content": "Markdown 内容",
  "note_type": "plain_text",
  "tags": ["标签1", "标签2"],
  "link_url": "https://...",
  "image_urls": ["https://..."]
}
```

- `plain_text`：同步返回，立即完成
- `link` / `img_text`：返回 task_id，**必须轮询** /task/progress

### 查询任务进度

```
POST /open/api/v1/resource/note/task/progress
Content-Type: application/json
```

```json
{"task_id": "task_abc123xyz"}
```

返回：status (pending | processing | success | failed), note_id, error_msg

**建议 10-30 秒间隔轮询，直到 success 或 failed**。

### 删除笔记

```
POST /open/api/v1/resource/note/delete
Content-Type: application/json
```

```json
{"note_id": "123456789"}
```

笔记移入回收站。

---

## 异步任务流程

### 链接笔记完整流程

**步骤 1**：提交任务 → 返回 task_id
```
POST /open/api/v1/resource/note/save {note_type:"link", link_url:"https://..."}
```

返回后**立即告知用户**：
> ✅ 链接已保存，正在抓取原文和生成总结，稍后告诉你结果...

**步骤 2**：后台轮询（10-30 秒间隔）
```
POST /open/api/v1/resource/note/task/progress {task_id} → 直到 status=success/failed
```

**步骤 3**：任务完成后，调详情接口展示
```
GET /open/api/v1/resource/note/detail?id={note_id}
```

> ✅ 笔记生成完成！
> - 📄 **原文**：已保存 {字数} 字
> - 📝 **总结**：{AI 生成的摘要}
> - 🔗 **来源**：{url}

### 图片笔记完整流程

**步骤 1**：获取上传凭证
```
GET /open/api/v1/resource/image/upload_token?mime_type=jpg&count=1
```

**步骤 2**：上传到 OSS（字段顺序必须严格遵守）

Python 方式（推荐）：
```python
files = {
    'file': ('image.jpg', open('image.jpg', 'rb'), 'image/jpeg')
}
data = {
    'key': object_key,
    'OSSAccessKeyId': accessid,
    'policy': policy,
    'signature': signature,
    'callback': callback,
    'Content-Type': 'image/jpeg'
}
r = requests.post(host, files=files, data=data)
```

curl 方式（图片无中文，可用）：
```bash
curl -X POST "$host" \
  -F "key=$object_key" \
  -F "OSSAccessKeyId=$accessid" \
  -F "policy=$policy" \
  -F "signature=$signature" \
  -F "callback=$callback" \
  -F "Content-Type=$oss_content_type" \
  -F "file=@/path/to/image.jpg"
```

**步骤 3**：提交任务
```
POST /open/api/v1/resource/note/save {note_type:"img_text", image_urls:[access_url]}
```

返回后**立即告知用户**：
> ✅ 图片已保存，正在识别内容，稍后告诉你结果...

**步骤 4-5**：轮询并展示结果（同链接笔记流程）

---

## 笔记召回

### 全局语义搜索

```
POST /open/api/v1/resource/recall
Content-Type: application/json
```

```json
{
  "query": "搜索关键词",
  "top_k": 3
}
```

返回 results[]，按相关度从高到低排序。

### 知识库语义搜索

```
POST /open/api/v1/resource/recall/knowledge
Content-Type: application/json
```

```json
{
  "topic_id": "知识库 alias id",
  "query": "搜索关键词",
  "top_k": 3
}
```

---

## 笔记整理

### 添加标签

```
POST /open/api/v1/resource/note/tags/add
Content-Type: application/json
```

```json
{
  "note_id": 123456789,
  "tags": ["工作", "重要"]
}
```

### 删除标签

```
POST /open/api/v1/resource/note/tags/delete
Content-Type: application/json
```

```json
{
  "note_id": 123456789,
  "tag_id": "123"
}
```

⚠️ system 类型标签不允许删除。

---

## 知识库

### 知识库列表

```
GET /open/api/v1/resource/knowledge/list?page=1
```

返回 topics[]，含 topic_id_alias、name、description、stats 等。

### 创建知识库

```
POST /open/api/v1/resource/knowledge/create
Content-Type: application/json
```

```json
{
  "name": "知识库名称",
  "description": "描述"
}
```

⚠️ 每天最多创建 50 个。

### 添加笔记到知识库

```
POST /open/api/v1/resource/knowledge/note/batch-add
Content-Type: application/json
```

```json
{
  "topic_id": "abc123",
  "note_ids": ["123456789", "123456790"]
}
```

⚠️ 每批最多 20 条。

### 从知识库移除

```
POST /open/api/v1/resource/knowledge/note/remove
Content-Type: application/json
```

```json
{
  "topic_id": "abc123",
  "note_ids": ["123456789"]
}
```

---

## 知识库：博主订阅

### 博主列表

```
GET /open/api/v1/resource/knowledge/bloggers?topic_id={alias_id}&page=1
```

### 博主内容列表

```
GET /open/api/v1/resource/knowledge/blogger/contents?topic_id={alias_id}&follow_id={follow_id}&page=1
```

### 博主内容详情

```
GET /open/api/v1/resource/knowledge/blogger/content/detail?topic_id={alias_id}&post_id={post_id_alias}
```

返回 post_media_text（含原文）。

---

## 知识库：直播订阅

### 已完成直播列表

```
GET /open/api/v1/resource/knowledge/lives?topic_id={alias_id}&page=1
```

### 直播详情

```
GET /open/api/v1/resource/knowledge/live/detail?topic_id={alias_id}&live_id={live_id}
```

返回 post_summary（AI 摘要）和 post_media_text（直播原文转写）。

---

## 错误处理

### 响应结构

```json
{
  "success": false,
  "error": {
    "code": 10001,
    "message": "unauthorized",
    "reason": "not_member"
  },
  "request_id": "xxx"
}
```

### 常见错误码

| 错误码 | 说明 | 处理方式 |
|--------|------|---------|
| 10001 | 鉴权失败 | 检查 API Key 和 Client ID |
| 10201 | 非会员 | 引导开通：https://www.biji.com/checkout?product_alias=6AydVpYeKl |
| 20001 | 笔记不存在 | 确认笔记 ID 正确 |
| 42900 | 限流 | 降低频率，查看 rate_limit 字段 |
| 50000 | 系统错误 | 稍后重试 |

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 必须使用 Python requests 库发送请求，不要使用 curl（curl 在 Windows 终端有编码问题导致中文乱码）
- 添加标签时 note_id 使用整数类型
- 删除标签时 tag_id 使用字符串类型
- 知识库操作使用 id 字段（如 XyYva8nN），不是 topic_id_alias

### Known Fixes & Workarounds
- curl 在 Windows 终端发送中文会变成乱码，必须用 Python requests 替代
- Get笔记 API 参数类型不一致：添加标签 POST /note/tags/add 的 note_id 必须是整数
- 删除标签 POST /note/tags/delete 的 tag_id 必须是字符串
- 知识库列表返回的 id 字段就是 topic_id，可直接用于其他知识库 API
- Get笔记 API 的 created_at 是字符串格式如 2026-03-24 13:05:03，不是 Unix 时间戳，解析时需用 datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") 而不是 datetime.fromtimestamp()
- 对 (datetime, dict) 元组列表排序时必须加 key=lambda x: x[0]，否则 Python 3 无法比较 dict 的大小
- datetime 的 timedelta 需要 from datetime import timedelta 显式导入，不能依赖其他调用路径的隐式 import

### Custom Instruction Injection

调用 Get笔记 API 时，统一使用 Python requests 库，设置 PYTHONIOENCODING=utf-8 环境变量确保中文处理正确