---
name: lark-wiki
version: 1.0.0
description: "飞书知识库：管理知识空间和文档节点。创建和查询知识空间、管理节点层级结构、在知识库中组织文档和快捷方式。当用户需要在知识库中查找或创建文档、浏览知识空间结构、移动或复制节点时使用。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli wiki --help"
---

# wiki (v2)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理**

## 核心概念

### 知识空间（Space）

知识空间是知识库的顶层容器，每个知识空间拥有独立的权限体系和节点树。一个企业可以创建多个知识空间，分别管理不同团队或项目的知识。

- **space_id**：知识空间的唯一标识
- **空间类型**：分为公开空间（组织内所有成员可访问）和私有空间（仅成员可访问）
- **空间管理员**：可以管理空间设置、成员、节点权限

### 节点（Node）

节点是知识空间中的基本单元，构成树形层级结构。每个节点可以包含一个文档或指向已有文档的快捷方式。

- **node_token**：节点的唯一标识（URL 中 `/wiki/wikcnXXXXX` 的 `wikcnXXXXX` 部分）
- **节点类型**：
  - `origin` — 原始文档节点，包含实际文档内容
  - `shortcut` — 快捷方式节点，指向知识库内或云空间中的已有文档
- **obj_type**：节点关联的文档类型（`docx`、`doc`、`sheet`、`bitable`、`slides`、`mindnote`、`file`）
- **obj_token**：文档的真实 token（用于后续通过 lark-doc、lark-sheets、lark-base 等操作文档内容）

### 权限继承

知识库采用层级权限继承模型：

1. **空间级权限**：控制谁能看到和访问整个知识空间
2. **节点级权限**：子节点默认继承父节点权限，也可以单独设置
3. **文档级权限**：文档本身也有独立的权限设置（通过 `lark-doc` 的权限 API 管理）

> **重要**：当通过 API 移动节点到新的父节点下时，节点的权限会受新父节点权限的影响。

### 资源关系

```
Space (space_id)
├── Node (node_token) ← 根节点
│   ├── Child Node (origin) ← 文档节点
│   │   ├── obj_type: docx/sheet/bitable/...
│   │   └── obj_token ← 真实文档 token
│   ├── Child Node (shortcut) ← 快捷方式
│   │   └── obj_token ← 指向的目标文档 token
│   └── Child Node (origin)
│       └── ...
└── Space Member (user / bot)
```

## 操作场景速查

| 场景 | API 方法 | 说明 |
|------|---------|------|
| 获取知识空间列表 | `spaces.list` | 列出当前身份可访问的所有知识空间 |
| 获取知识空间信息 | `spaces.get` | 查询单个知识空间的详细设置 |
| 创建知识空间 | `spaces.create` | 创建新的知识空间（仅 `user` 身份） |
| 获取空间成员列表 | `space_members.list` | 列出空间成员和管理员 |
| 添加空间成员 | `space_members.create` | 添加成员或管理员（需空间管理员权限） |
| 删除空间成员 | `space_members.delete` | 移除空间成员或管理员 |
| 更新空间设置 | `space_settings.update` | 修改空间名称、描述等设置（需管理员权限） |
| 创建节点 | `space_nodes.create` | 在指定父节点下创建新节点 |
| 获取节点信息 | `space_nodes.get_node` | 查询节点的元数据（类型、token、权限等） |
| 获取子节点列表 | `space_nodes.list` | 获取某节点下的所有子节点 |
| 移动节点 | `space_nodes.move` | 移动节点到新的父节点下 |
| 更新节点标题 | `space_nodes.update_title` | 修改节点标题 |
| 创建节点副本 | `space_nodes.copy` | 复制节点到指定位置 |
| 移动云空间文档至知识空间 | `tasks.move_docs_to_wiki` | 将云空间中的文档迁移到知识库 |
| 查询异步任务结果 | `tasks.get` | 查询异步任务（移动文档等）的执行状态 |
| 搜索知识库 | `space_nodes.search` | 按关键词搜索知识库中的内容 |

## API Resources

```bash
lark-cli schema wiki.<resource>.<method>   # 调用 API 前必须先查看参数结构
lark-cli wiki <resource> <method> [flags] # 调用 API
```

> **重要**：使用原生 API 时，必须先运行 `schema` 查看 `--data` / `--params` 参数结构，不要猜测字段格式。

### spaces

  - `create` — 创建知识空间。Identity: `user` only（`user_access_token`）。仅通过用户身份创建，创建者自动成为空间管理员。
  - `get` — 获取知识空间信息。Identity: supports `user` and `bot`。返回空间类型、可见性、分享状态等元数据。频率限制：100 次/分钟。
  - `list` — 获取知识空间列表。Identity: `bot`（`tenant_access_token`）。列出应用可访问的所有知识空间，支持分页。

### space_members

  - `create` — 添加知识空间成员或管理员。Identity: supports `user` and `bot`。调用者必须为空间管理员。公开知识空间仅支持添加管理员。
  - `delete` — 删除知识空间成员或管理员。Identity: supports `user` and `bot`。根据空间类型和可见性，操作可能受限。
  - `list` — 获取知识空间成员列表。Identity: supports `user` and `bot`。支持分页查询，返回成员和管理员信息。

### space_settings

  - `update` — 更新知识空间设置（名称、描述等）。Identity: supports `user` and `bot`。调用者必须为空间管理员。

### space_nodes

  - `create` — 创建知识空间节点。Identity: supports `user` and `bot`。需拥有父节点容器的编辑权限。支持创建 `docx`、`doc`、`sheet`、`bitable`、`mindnote` 等类型的原始节点，以及 `shortcut` 类型节点。**不支持创建 `file` 类型节点**。
  - `copy` — 创建知识空间节点副本。Identity: supports `user` and `bot`。将节点复制到指定位置，支持自定义权限设置。
  - `get_node` — 获取知识空间节点信息。Identity: supports `user` and `bot`。需具备节点阅读权限。返回节点类型、obj_type、obj_token、标题、所有者等。
  - `list` — 获取知识空间子节点列表。Identity: supports `user` and `bot`。需具备父节点阅读权限，支持分页。
  - `move` — 移动知识空间节点。Identity: supports `user` and `bot`。支持在知识库内跨空间移动节点，子节点会跟随一起移动。需满足节点、原父节点、目标父节点的编辑权限。
  - `update_title` — 更新知识空间节点标题。Identity: supports `user` and `bot`。支持文档节点和快捷方式节点。频率限制：100 次/分钟。
  - `search` — 搜索知识库内容。Identity: `user` only（`user_access_token`）。按关键词搜索当前用户可见的知识库内容，支持分页。

### tasks

  - `get` — 获取异步任务结果。Identity: supports `user` and `bot`。查询移动文档到知识库等异步任务的执行状态和结果。仅任务创建者可查询。
  - `move_docs_to_wiki` — 移动云空间文档至知识空间。Identity: supports `user` and `bot`。异步操作，移动后文档继承父页面权限，在"知识库"中显示，无法从云空间主页访问。

## 权限表

| 方法 | 所需 scope |
|------|-----------|
| `spaces.create` | `wiki:wiki:write` |
| `spaces.get` | `wiki:wiki:read` |
| `spaces.list` | `wiki:wiki:read` |
| `space_members.create` | `wiki:wiki:write` |
| `space_members.delete` | `wiki:wiki:write` |
| `space_members.list` | `wiki:wiki:read` |
| `space_settings.update` | `wiki:wiki:write` |
| `space_nodes.create` | `wiki:node:write` |
| `space_nodes.copy` | `wiki:node:write` |
| `space_nodes.get_node` | `wiki:node:read` |
| `space_nodes.list` | `wiki:node:read` |
| `space_nodes.move` | `wiki:node:write` |
| `space_nodes.update_title` | `wiki:node:write` |
| `space_nodes.search` | `wiki:node:read` |
| `tasks.get` | `wiki:wiki:read` |
| `tasks.move_docs_to_wiki` | `wiki:wiki:write` |

## 典型工作流

### 1. 创建知识空间并组织内容

```bash
# Step 1: 创建知识空间（仅 user 身份）
lark-cli schema wiki.spaces.create   # 先查看参数
lark-cli wiki spaces create --as user --data '{"name":"项目文档库"}'

# Step 2: 创建一级节点（如"需求文档"）
lark-cli schema wiki.space_nodes.create
lark-cli wiki space_nodes create --as user \
  --data '{"space_id":"<space_id>","parent_node_token":"","obj_type":"docx","title":"需求文档"}'

# Step 3: 在一级节点下创建子节点
lark-cli wiki space_nodes create --as user \
  --data '{"space_id":"<space_id>","parent_node_token":"<node_token>","obj_type":"docx","title":"v2.0 需求规格"}'

# Step 4: 添加空间成员
lark-cli wiki space_members create --as user \
  --data '{"space_id":"<space_id>","member_type":"userid","member_id":"<user_id>","role":"reader"}'
```

### 2. 浏览知识空间结构

```bash
# 获取可访问的知识空间列表
lark-cli wiki spaces list --as bot

# 获取空间的根节点子节点
lark-cli schema wiki.space_nodes.list   # 先查看参数
lark-cli wiki space_nodes list --as bot \
  --params '{"space_id":"<space_id>","parent_node_token":""}'

# 获取特定节点的详细信息（含 obj_type 和 obj_token）
lark-cli wiki space_nodes get_node --as bot \
  --params '{"token":"<node_token>"}'
```

### 3. 移动和复制节点

```bash
# 复制节点到另一个位置
lark-cli schema wiki.space_nodes.copy
lark-cli wiki space_nodes copy --as user \
  --data '{"source_token":"<node_token>","space_id":"<target_space_id>","parent_node_token":"<target_parent_token>"}'

# 移动节点到新的父节点（子节点一起移动）
lark-cli schema wiki.space_nodes.move
lark-cli wiki space_nodes move --as user \
  --data '{"target_parent_token":"<new_parent_token>","space_id":"<space_id>","token":"<node_token>"}'
```

### 4. 搜索知识库

```bash
# 按关键词搜索知识库（仅 user 身份）
lark-cli schema wiki.space_nodes.search
lark-cli wiki space_nodes search --as user \
  --params '{"query":"接口文档","page_size":20}'
```

### 5. 将云空间文档迁移到知识库

```bash
# 发起迁移任务（异步）
lark-cli schema wiki.tasks.move_docs_to_wiki
lark-cli wiki tasks move_docs_to_wiki --as user \
  --data '{"space_id":"<space_id>","parent_node_token":"<target_node_token>","obj_tokens":["<file_token_1>","<file_token_2>"]}'

# 查询任务结果
lark-cli wiki tasks get --as user \
  --params '{"task_id":"<task_id>","type":"move_to_wiki"}'
```

## 与 lark-doc 的边界说明

| 职责 | wiki | lark-doc |
|------|------|----------|
| 知识空间管理 | 创建/查询/设置知识空间 | -- |
| 节点层级管理 | 创建/移动/复制/删除节点 | -- |
| 空间成员管理 | 添加/移除空间成员 | -- |
| Wiki Token 解析 | `get_node` 获取 `obj_token` | -- |
| 文档内容读取 | -- | 读取文档块内容、纯文本 |
| 文档内容编辑 | -- | 创建/更新/删除文档块 |
| 文档创建（Markdown） | -- | 从 Markdown 创建文档 |
| 文档评论 | -- | 管理文档评论 |
| 文档搜索 | 搜索知识库内容 | 搜索云空间文档 |

**协作流程**：当需要操作知识库中的文档内容时，先用 `wiki.space_nodes.get_node` 获取节点的 `obj_type` 和 `obj_token`，再根据 `obj_type` 调用对应的 skill（`lark-doc` 处理 docx/doc、`lark-sheets` 处理 sheet、`lark-base` 处理 bitable 等）。

## 常见错误处理

### 权限不足（99991668 / 99991672）

**现象**：API 返回权限相关错误码。

**排查步骤**：
1. 确认当前身份（`user` 还是 `bot`）是否满足 API 要求
2. 确认应用已开通对应的 scope（参见上方权限表）
3. 对于 `user` 身份，确认用户已通过 `lark-cli auth login` 授权
4. 对于知识空间操作，确认调用者是空间成员且拥有足够角色（管理员/编辑者/阅读者）
5. 对于节点操作，确认调用者对父节点有编辑权限

### 节点不存在（99991664）

**现象**：`get_node` 或 `list` 返回节点不存在。

**排查步骤**：
1. 确认 `node_token` 格式正确（以 `wikcn` 开头）
2. 确认节点未被删除
3. 确认当前身份有该节点的访问权限（私有节点可能对 bot 不可见）
4. 如从 URL 提取 token，确认 URL 格式为 `/wiki/wikcnXXXXX`

### 不支持的操作

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 创建 `file` 类型节点失败 | `space_nodes.create` 不支持 `file` 类型 | 先上传文件到云空间，再通过 `tasks.move_docs_to_wiki` 迁移 |
| Bot 无法创建知识空间 | `spaces.create` 仅支持 `user` 身份 | 使用 `--as user` 调用 |
| Bot 无法搜索知识库 | `space_nodes.search` 仅支持 `user` 身份 | 使用 `--as user` 调用 |
| 跨知识库复制节点失败 | 复制操作需对源节点和目标位置都有权限 | 确认两边权限均满足 |

### Wiki 链接解析注意事项

知识库链接（`/wiki/TOKEN`）中的 token 不能直接当作 `file_token` 使用。必须先通过 `wiki.space_nodes.get_node` 解析获取真实的 `obj_token`，再根据 `obj_type` 使用对应的 API 操作文档内容。

```bash
# 错误做法：直接把 wiki token 当 file_token
lark-cli docs +get --file-token "wikcnXXXXX"   # 会失败

# 正确做法：先解析 wiki token
lark-cli wiki space_nodes get_node --params '{"token":"wikcnXXXXX"}'
# 从返回结果中取 node.obj_token 和 node.obj_type
# 再用 obj_token 调用对应 API
```

## 重要限制

1. **节点层级深度**：知识库节点树层级过深可能影响性能，建议控制在合理范围内
2. **移动节点权限**：移动节点需同时满足源位置和目标位置的权限要求
3. **异步操作**：`tasks.move_docs_to_wiki` 是异步操作，必须通过 `tasks.get` 轮询结果
4. **频率限制**：不同 API 有不同的频率限制（详见各方法说明），超限需等待重试
5. **公开空间**：公开知识空间的所有组织成员自动拥有阅读权限，仅支持通过 API 添加管理员
