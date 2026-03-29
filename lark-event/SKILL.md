---
name: lark-event
version: 1.0.0
description: "飞书事件订阅：通过 WebSocket 长连接实时监听飞书事件（消息、通讯录变更、日历变更等），输出 NDJSON 到 stdout，支持 compact Agent 友好格式、正则路由、文件输出。当用户需要实时监听飞书事件、构建事件驱动管道时使用。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli event --help"
---

# event (v1)

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) 了解认证、权限处理和安全规则。

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`lark-cli event +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+subscribe`](references/lark-event-subscribe.md) | Subscribe to Lark events via WebSocket long connection (read-only, NDJSON output); bot-only; supports compact agent-friendly format, regex routing, file output |

---

## 核心概念

### WebSocket 事件订阅

飞书事件订阅通过 **WebSocket 长连接**实现实时监听。与 HTTP 回调（webhook）不同，WebSocket 模式下 CLI 作为客户端主动连接飞书服务器，无需公网地址或回调 URL。

**工作原理：**
1. CLI 使用 App ID + App Secret 向飞书服务器发起 WebSocket 连接
2. 连接建立后，服务器将匹配的事件实时推送到客户端
3. 事件以 NDJSON（每行一个 JSON 对象）格式输出到 stdout
4. SDK 内置自动重连机制，断线后自动恢复

**身份要求：** 仅支持 bot 身份（应用身份），无需用户登录。`lark-cli config init` 配置 App 凭证即可。

### 事件类型

飞书事件按业务域分类，每类事件有唯一的 `event_type` 标识符（如 `im.message.receive_v1`）。常用事件分为以下几类：

| 业务域 | 事件类型示例 | 说明 |
|--------|-------------|------|
| IM（消息） | `im.message.receive_v1` | 接收消息、消息已读、表情回应等 |
| Contact（通讯录） | `contact.user.created_v3` | 用户/部门创建、更新、删除 |
| Calendar（日历） | `calendar.calendar.event.changed_v4` | 日历 ACL 创建、日程变更 |
| Approval（审批） | `approval.approval.updated` | 审批状态更新 |
| Task（任务） | `task.task.update_tenant_v1` | 任务更新、评论更新 |
| Drive（云文档） | `drive.notice.comment_add_v1` | 文档评论添加 |
| Application（应用） | `application.application.visibility.added_v6` | 应用可见性变更 |

> 完整事件列表见 [飞书事件列表](https://open.feishu.cn/document/server-docs/event-subscription-guide/event-list)。

**重要：** 事件类型必须在飞书开放平台控制台中预先配置（事件与回调 → 订阅方式 → 选择「使用长连接接收事件」→ 添加需要的事件）。CLI 无法动态订阅未在控制台配置的事件类型。

### 正则路由

正则路由允许基于 `event_type` 将事件分发到不同的输出目标。这是构建事件驱动管道的核心机制。

**路由规则格式：** `regex=dir:./path`

- `regex`：匹配 `event_type` 的正则表达式
- `dir:./path`：匹配的事件写入该目录（每个事件一个文件）
- 未匹配任何路由规则的事件回退到 `--output-dir` 或 stdout
- 可指定多个 `--route`，按顺序匹配，首个匹配生效

### 文件输出

启用文件输出后，每个事件作为独立的 JSON 文件写入指定目录，文件命名格式为 `{type}_{id}_{ts}.json`。适合需要持久化存储或后续批量处理的场景。

---

## 使用流程

### Step 1: 启动事件订阅

最基础的用法——订阅所有已注册事件：

```bash
lark-cli event +subscribe
```

指定特定事件类型（仅接收这些类型）：

```bash
lark-cli event +subscribe --event-types im.message.receive_v1
lark-cli event +subscribe --event-types im.message.receive_v1,contact.user.created_v3
```

预览配置（不实际连接）：

```bash
lark-cli event +subscribe --dry-run
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--event-types <types>` | 否 | 逗号分隔的事件类型列表，仅接收这些类型。省略则注册 24 种常用事件（catch-all 模式） |
| `--filter <regex>` | 否 | 客户端正则过滤器，匹配 `event_type`，在 SDK 交付事件后应用。可与 `--event-types` 组合使用 |
| `--quiet` | 否 | 抑制 stderr 状态消息 |
| `--force` | 否 | 绕过单实例锁（**不安全**：服务器会随机分配事件到不同连接，每个实例只收到子集） |
| `--dry-run` | 否 | 仅打印配置，不连接 WebSocket |

### Step 2: 事件路由配置

使用 `--route` 按正则将事件分发到不同目录：

```bash
# IM 事件写入 im-events/，通讯录事件写入 contacts/
lark-cli event +subscribe \
  --route '^im\.message=dir:./im-events/' \
  --route '^contact\.=dir:./contacts/'

# IM 事件写入文件，其余事件输出到 stdout
lark-cli event +subscribe --route '^im\.=dir:./im-events/'
```

路由规则匹配顺序：按 `--route` 参数的出现顺序逐一匹配，首个匹配生效。未匹配任何规则的事件回退到 `--output-dir`（若指定）或 stdout。

### Step 3: 事件数据格式

#### 默认格式（原始 NDJSON）

每行一个 JSON 对象，包含所有原始字段：

```json
{"schema":"2.0","header":{"event_id":"xxx","event_type":"im.message.receive_v1","create_time":"1773491924409","app_id":"cli_xxx"},"event":{"message":{"chat_id":"oc_xxx","content":"{\"text\":\"Hello\"}","message_id":"om_xxx","message_type":"text"},"sender":{"sender_id":{"open_id":"ou_xxx"},"sender_type":"user"}}}
```

#### Compact 格式（Agent 友好）

添加 `--compact` 标志后，输出扁平化的键值对，提取语义化字段并剥离噪声：

```json
{"type":"im.message.receive_v1","id":"om_xxx","message_id":"om_xxx","chat_id":"oc_xxx","chat_type":"p2p","message_type":"text","content":"Hello","sender_id":"ou_xxx","create_time":"1773491924409","timestamp":"1773491924409"}
```

**Compact 处理规则：**
- IM 消息事件（`im.message.receive_v1`）有深度处理：解析双编码 JSON 的 `content` 字段为可读文本，扁平化 `sender_id`，剥离 `schema`/`token`/`tenant_key`/`app_id`
- 其他 IM 事件（表情回应、群成员变更、群信息更新等）有专用 compact 处理器
- 非 IM 事件使用通用 compact 处理器：解析事件载荷为扁平映射，注入 `type`/`event_id`/`timestamp`

> Agent 管道应始终使用 `--compact --quiet`。

使用 `--json` 可切换为 pretty-print JSON（非 NDJSON）。

### Step 4: 文件输出配置

将事件写入文件：

```bash
# 所有事件写入指定目录
lark-cli event +subscribe --output-dir ./events

# 路由 + 文件输出组合
lark-cli event +subscribe \
  --route '^im\.message=dir:./im-messages/' \
  --route '^contact\.=dir:./contacts/' \
  --output-dir ./other-events
```

文件命名格式：`{event_type}_{event_id}_{timestamp}.json`。输出目录不存在时会自动创建。

---

## 与 lark-im / lark-contact 的关系

| 技能 | 模式 | 典型用途 |
|------|------|---------|
| **lark-event** | 实时监听（被动） | 订阅消息/通讯录变更，构建事件驱动管道 |
| **lark-im** | 主动查询（pull） | 发送消息、查询会话列表、管理消息 |
| **lark-contact** | 主动查询（pull） | 查询用户/部门信息、批量导出通讯录 |

**典型组合：** 用 `lark-event +subscribe` 监听新消息，在管道中处理内容，再用 `lark-cli api POST "/open-apis/im/v1/messages/..." --as bot` 回复消息。

---

## 错误处理

### 连接断开

SDK 内置自动重连机制。断线后会自动尝试重新建立 WebSocket 连接，无需手动干预。`Ctrl+C` 可优雅关闭并打印已接收事件总数。

### 认证过期

App 凭证（App ID + App Secret）无效或过期时，连接会被服务器拒绝。错误信息输出到 stderr。解决方式：
1. 确认 `lark-cli config init` 中的 App 凭证正确
2. 确认应用在飞书开放平台中未被禁用
3. 确认已启用长连接订阅方式（控制台 → 事件与回调 → 订阅方式）

### WebSocket 超时

长时间无事件时连接可能被服务器或中间网络设备断开。SDK 的自动重连机制会处理此情况。如果频繁超时：
1. 检查网络连接稳定性
2. 检查防火墙/代理是否允许 WebSocket 长连接
3. 使用 `--quiet` 减少 stderr 输出，便于监控实际连接状态

### 事件未收到

如果订阅后没有收到预期的事件，按以下顺序排查：
1. 确认事件类型已在飞书开放平台控制台中添加
2. 确认对应权限已启用（如 `im:message:receive_as_bot`）
3. 确认 `--event-types` 参数（如果指定了）包含目标事件类型
4. 确认没有多个 `+subscribe` 实例在运行（事件会被随机分配）
5. 使用 `--dry-run` 预览配置确认参数正确

---

## Agent 管道示例

### 监听消息并用 Claude 回复

```bash
lark-cli event +subscribe \
  --event-types im.message.receive_v1 --compact --quiet \
  | while IFS= read -r line; do
      content=$(echo "$line" | jq -r '.content // empty')
      message_id=$(echo "$line" | jq -r '.message_id // empty')
      [[ -z "$content" ]] && continue

      answer=$(claude -p "Reply concisely: $content" < /dev/null 2>/dev/null)

      reply_data=$(jq -n --arg t "$answer" '{msg_type:"text",content:({text:$t}|tojson)}')
      lark-cli api POST "/open-apis/im/v1/messages/$message_id/reply" \
        --data "$reply_data" --as bot --format data
    done
```

### 监听消息并写入飞书文档

```bash
lark-cli event +subscribe \
  --event-types im.message.receive_v1 --compact --quiet \
  | while IFS= read -r line; do
      content=$(echo "$line" | jq -r '.content // empty')
      [[ -z "$content" ]] && continue

      lark-cli docs +update --doc "DOC_URL" --mode append --markdown "- $content"
    done
```

---

## 参考链接

- [`+subscribe` 详细文档](references/lark-event-subscribe.md) — 完整参数说明、输出格式、事件类型列表、管道示例
- [`lark-im`](../lark-im/SKILL.md) — 消息发送与查询
- [`lark-contact`](../lark-contact/SKILL.md) — 通讯录查询
- [`lark-shared`](../lark-shared/SKILL.md) — 认证、全局参数、安全规则
