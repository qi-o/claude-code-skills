---
name: lark-contact
version: 1.0.0
description: "飞书通讯录：查询组织架构、人员信息和搜索员工。获取当前用户或指定用户的详细信息、通过关键词搜索员工（姓名/邮箱/手机号）。当用户需要查看个人信息、查找同事 open_id 或联系方式、按姓名搜索员工、查询部门结构时使用。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli contact --help"
---

# contact (v1)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理**

## Core Concepts

### 用户 ID 体系

飞书通讯录中存在三种用户标识，用途各不相同：

| ID 类型 | 格式 | 说明 |
|---------|------|------|
| `user_id` | 数字字符串（如 `4g3f...`） | 用户在组织内的唯一标识，由系统分配，跨应用通用。一般不直接暴露给开发者使用。 |
| `open_id` | `ou_xxxxxxxx` | 用户在**当前应用**内的唯一标识。同一个用户在不同应用中的 `open_id` 不同。**本 skill 和其他 lark skill 最常用的 ID 类型**。 |
| `union_id` | `on_xxxxxxxx` | 用户在**当前开发者账号**下的统一标识。同一开发者账号下的所有应用共享同一个 `union_id`，适合跨应用识别用户。 |

### chat_id 与用户 ID 的区别

| ID 类型 | 标识对象 | 典型用途 |
|---------|---------|---------|
| `open_id` (`ou_xxx`) | 一个**用户** | 发送私聊消息、指定日程参会人、分配任务负责人 |
| `chat_id` (`oc_xxx`) | 一个**群聊或 P2P 会话** | 发送群消息、获取群成员列表、搜索群聊 |

> **不要混淆**：给用户发私聊消息时，lark-im 的 `+messages-send` 接受 `--user-id ou_xxx`（自动解析为 P2P 会话），也可以直接传 `--chat-id oc_xxx`（已知会话 ID 时）。两者不要混用。

### 身份类型：用户身份 vs 机器人身份

- `--as user`：以**授权用户**身份操作，使用 `user_access_token`。权限取决于该用户在组织中的角色和可见范围。
- `--as bot`：以**应用机器人**身份操作，使用 `tenant_access_token`。权限取决于应用的作用域（scope）和可用范围设置。

通讯录 API 主要使用 `user_access_token`（用户身份），因为查看通讯录本质上是"代替用户查看他能看到的人"。使用 `tenant_access_token` 时，只能看到应用可用范围内的用户。

### 可见范围限制

**只能查询本组织内的用户。** 飞书通讯录 API 遵循组织架构可见范围规则：

- 用户身份下，只能看到该用户有权限查看的组织成员（由管理员在「组织架构」中配置可见范围）。
- 机器人身份下，只能看到应用可用范围内的成员（由管理员在「应用管理」中配置可用范围）。
- 无法查询外部联系人、未加入本组织的用户、或已离职/停用的用户（除非管理员开放相应权限）。

## Resource Relationships

```
Organization (tenant)
├── Department (子部门树)
│   └── User (用户)
│       ├── open_id   (应用级标识, ou_xxx)
│       ├── union_id  (开发者级标识, on_xxx)
│       └── user_id   (组织级标识, 数字串)
└── Bot (应用机器人)
    └── (无 open_id，使用 app_id 标识)
```

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`lark-cli contact +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+search-user`](references/lark-contact-search-user.md) | 搜索员工（按姓名/邮箱/手机号），结果按亲密度排序 |
| [`+get-user`](references/lark-contact-get-user.md) | 获取用户信息（不传 user_id 获取当前用户；传入则获取指定用户） |

### +search-user（搜索员工）

通过关键词搜索组织内的员工，支持按姓名、邮箱、手机号等字段匹配。

**典型参数**：
- `--query <text>`（必填）：搜索关键词
- `--page-size <n>`（可选）：分页大小，默认 20，最大 200
- `--page-token <token>`（可选）：翻页标记，来自上一次返回的 `page_token`
- `--format`（可选）：`json`（默认）或 `pretty`

**返回值关键字段**：
- `items[].user.open_id`：用户的 open_id（最常用，用于后续 API 调用）
- `items[].user.name`：用户姓名
- `items[].user.emails`：邮箱列表
- `items[].user.mobiles`：手机号列表
- `items[].user.department_ids`：所属部门 ID 列表
- `has_more`：是否有下一页
- `page_token`：下一页的翻页标记

**使用模式**：
1. 先用 `+search-user --query "张三"` 搜索
2. 从返回的 `items` 中找到目标用户，提取 `open_id`
3. 将 `open_id` 传给其他 skill（如 lark-im 发消息）

### +get-user（获取用户信息）

两种使用模式：

1. **不传 `--user-id`**：获取当前登录用户信息（调用 `GET /open-apis/authen/v1/user_info`）
2. **传入 `--user-id`**：获取指定用户详细信息（调用 `GET /open-apis/contact/v3/users/{user_id}`）

**典型参数**：
- `--user-id <id>`（可选）：目标用户的 ID，不传则获取当前用户
- `--user-id-type <type>`（可选）：`open_id`（默认）/ `union_id` / `user_id`
- `--table`（可选）：表格输出格式

**返回值关键字段**：
- `user.open_id` / `user.union_id` / `user.user_id`：三种 ID
- `user.name`：姓名
- `user.en_name`：英文名
- `user.emails`：邮箱列表
- `user.mobiles`：手机号列表
- `user.gender`：性别（1=男，2=女）
- `user.avatar.avatar_origin`：头像原图 URL
- `user.department_ids`：所属部门 ID 列表
- `user.leader_user_id`：直属上级的 user_id

### 获取当前登录用户信息

```bash
# 最简方式：不传 --user-id
lark-cli contact +get-user

# 查看可读格式
lark-cli contact +get-user --table
```

适用于：确认当前授权用户是谁、获取当前用户的 open_id 用于其他操作。

## 与其他 Skill 的协作关系

本 skill 是飞书工具链中的**基础能力模块**，主要职责是为其他 skill 提供 `open_id` 等用户标识。

### lark-im（即时通讯）

| 场景 | 协作方式 |
|------|---------|
| 给指定用户发私聊消息 | 先用 `+search-user` 获取 `open_id`，再传给 `lark-im +messages-send --user-id ou_xxx` |
| 给指定用户发群聊消息 | 群消息使用 `chat_id`，但如果只知道用户名，需要先通过 contact 查 `open_id`，再通过 im 查找包含该用户的群聊 |
| 查看消息发送者信息 | im 返回消息中的 sender 字段只有 open_id，需要 contact 的 `+get-user` 获取姓名等详情 |

### lark-calendar（日历）

| 场景 | 协作方式 |
|------|---------|
| 创建日程并添加参会人 | 日程参会人需要 `user_id` 或 `open_id`，先用 `+search-user` 查找参会人 |
| 查看日程组织者信息 | 日程返回的 organizer 字段是 open_id，需要 contact 解析姓名 |

### lark-task（任务）

| 场景 | 协作方式 |
|------|---------|
| 创建任务并指派负责人 | 任务负责人需要 `open_id`，先用 `+search-user` 查找 |
| 创建任务协作人 | 协作人同样需要 `open_id` |
| 批量创建任务给多人 | 循环调用 `+search-user` 获取每个人的 `open_id` |

### lark-doc / lark-drive / lark-wiki

| 场景 | 协作方式 |
|------|---------|
| 设置文档权限 | 文档权限需要指定用户 open_id 或部门 ID |
| 查看文档协作者 | 返回协作者列表中的 user_id 需要通过 contact 获取姓名 |

## 常见错误处理

### 用户不存在（open_id 无效）

**现象**：调用 `+get-user --user-id ou_xxx` 返回错误，提示用户不存在。

**排查步骤**：
1. 确认 `open_id` 是否正确复制（没有多余空格或截断）
2. 确认 `user_id_type` 是否为 `open_id`（如果传入的是 `union_id` 但未指定 `--user-id-type union_id`，会匹配不到）
3. 确认用户是否已离职或被停用

### 权限不足（无法查看通讯录）

**现象**：返回错误码 `41050` 或类似权限错误。

**原因**：当前用户的组织架构可见范围不包含目标用户，或应用的可用范围不够。

**解决方案**：
1. 联系飞书管理员，在「组织架构」中调整当前用户的可见范围
2. 或改用应用身份（`--as bot`），确保应用的可用范围覆盖目标用户
3. 确认应用已开通 `contact:user.base:readonly` 等必要 scope

### 搜索结果为空

**现象**：`+search-user --query "张三"` 返回空列表。

**排查步骤**：
1. 确认搜索关键词是否正确（注意繁简体、全半角、空格）
2. 确认目标用户是否在本组织内（跨组织用户无法搜索）
3. 确认目标用户是否在当前可见范围内
4. 尝试更换搜索词（如用手机号或邮箱搜索，匹配可能更精确）

### 多人同名时的处理策略

**现象**：搜索返回多个同名用户，需要精确匹配目标。

**处理方法**：
1. 优先使用更精确的关键词搜索（手机号 > 邮箱 > 姓名+部门）
2. 对比返回结果中的 `department_ids`（部门信息）或 `emails` / `mobiles` 区分
3. 如果仍无法确定，向用户确认：「搜索到多个同名用户，请提供更多信息（部门、邮箱或手机号）」
4. 禁止猜测选择：不要自行从同名用户中随机挑选一个

## Agent 执行规则

1. **先搜索再操作**：任何需要 open_id 的操作，必须先通过 `+search-user` 搜索获取，禁止凭记忆或猜测填写 open_id。
2. **结果确认**：搜索结果只有一个匹配时可直接使用；多个匹配时必须向用户确认。
3. **ID 类型一致**：跨 skill 传递 ID 时，确认接收方期望的 ID 类型（绝大多数情况是 `open_id`）。
4. **翻页处理**：搜索结果 `has_more=true` 时，继续翻页查找，不要截断或忽略后续结果。
5. **缓存意识**：同一会话中多次查询同一用户时，复用已获取的 open_id，避免重复搜索。
