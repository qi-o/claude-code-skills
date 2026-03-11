---
name: webnovel-import
description: 导入已有小说（大纲/章节/设定）到网文项目。用于续写已有内容，而非从零创建项目。
allowed-tools: Read Write Edit Grep Bash Task AskUserQuestion Glob
---

# Novel Import (续写导入模块)

## 目标

- 将用户的已有小说内容导入项目结构，支持续写模式
- 区分两种导入模式：从零导入（无章节）/ 章节续写（已有章节）
- 生成可直接使用 `/webnovel-write` 继续写作的项目结构

## 执行原则

1. 先确认导入模式，再收集对应信息
2. 导入章节时自动识别编号并规范化存储
3. 生成摘要和状态文件，确保上下文可召回
4. 不修改用户提供的原始内容，只做复制/解析

## 模式定义

| 模式 | 说明 | 产出 |
|------|------|------|
| A. 从零导入 | 只有大纲/设定，无章节 | 项目骨架 + 大纲 + 设定集 |
| B. 章节续写 | 已有章节，需要继续写 | 项目骨架 + 大纲 + 设定集 + 已有章节 |

## 环境设置

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/scripts" ]; then
  echo "ERROR: 未设置 CLAUDE_PLUGIN_ROOT 或缺少目录: ${CLAUDE_PLUGIN_ROOT}/scripts" >&2
  exit 1
fi
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"

# 解析真实书项目根
export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

## 交互流程

### Step 0：预检

检查用户需求：
1. 用户是否已有小说内容需要导入？
2. 是否有明确的续写目标（继续写新章节）？

确认后进入 Step 1。

### Step 1：选择导入模式

询问用户选择：

**A. 从零导入（无章节）**
- 用户只有大纲/设定，还没有写章节
- 需要创建项目骨架，然后从第1章开始写

**B. 章节续写（已有章节）**
- 用户已有部分章节，需要导入后继续写
- 需要扫描已有章节并导入

使用 `AskUserQuestion` 让用户选择。

### Step 2：收集项目基础信息（两种模式都需要）

无论选择哪种模式，都需要收集：

1. **书名**（项目名称）
2. **题材**（用于加载对应 genre 参考）
3. **目标规模**（总字数或总章数）

这些信息用于初始化 `state.json` 和项目结构。

### Step 3：导入大纲

收集大纲内容：
- 用户提供的大纲文本（可以粘贴或描述）
- 核心主线、关键情节点

处理：
1. 解析大纲文本
2. 写入 `大纲/总纲.md`
3. 更新 `state.json` 的 `project_info`

### Step 4：导入设定（可选）

收集设定信息（用户有的才收集）：

| 设定类型 | 写入文件 | 说明 |
|----------|----------|------|
| 世界观 | `设定集/世界观.md` | 故事发生的世界背景 |
| 角色 | `设定集/主角卡.md` / `设定集/女主卡.md` / `设定集/配角卡.md` | 人物设定 |
| 金手指 | `设定集/金手指设计.md` | 主角的特殊能力/系统 |
| 力量体系 | `设定集/力量体系.md` | 修炼/能力等级设定 |
| 势力 | `设定集/势力分布.md` | 宗门/组织/国家等 |

### Step 5：导入章节（仅模式B）

1. **扫描章节文件**：
   - 用户提供章节文件所在目录
   - 或用户直接粘贴章节内容

2. **识别章节编号**：
   - 从文件名提取（如 `第12章.txt`、`ch13.md`）
   - 从文件内容标题提取（如 `# 第14章 xxx`）
   - 无编号则询问用户

3. **复制到项目目录**：
   - 格式：`正文/第NNNN章.md`（4位数字）
   - 保留原始内容，只做格式规范化

4. **更新进度**：
   - 设置 `progress.current_chapter` 为最大章节号
   - 生成已有章节的摘要（用于上下文召回）

### Step 6：初始化状态

1. **创建 state.json**（若不存在）：
```json
{
  "project": {
    "title": "",
    "genre": "",
    "target_words": 0,
    "target_chapters": 0,
    "one_liner": "",
    "core_conflict": ""
  },
  "progress": {
    "current_chapter": 0,
    "total_words": 0
  },
  "chapter_meta": {}
}
```

2. **生成章节摘要**（模式B）：
   - 读取每个已有章节
   - 生成 100-200 字摘要
   - 写入 `.webnovel/summaries/chNNNN.md`

3. **提取关键信息**（自动/可选）：
   - 角色列表
   - 伏笔/线索
   - 世界观要素

## 项目目录结构

导入后应生成以下结构：

```
{project_root}/
├── .webnovel/
│   ├── state.json          # 项目状态
│   ├── summaries/          # 章节摘要
│   │   ├── ch0001.md
│   │   ├── ch0002.md
│   │   └── ...
│   └── index.db            # 向量索引（可选）
├── 大纲/
│   └── 总纲.md             # 大纲内容
├── 设定集/
│   ├── 世界观.md
│   ├── 主角卡.md
│   ├── 女主卡.md
│   ├── 金手指设计.md
│   ├── 力量体系.md
│   └── 势力分布.md
└── 正文/
    ├── 第0001章.md
    ├── 第0002章.md
    └── ...
```

## 验证与交付

执行检查：

```bash
test -f "${PROJECT_ROOT}/.webnovel/state.json"
test -f "${PROJECT_ROOT}/大纲/总纲.md"
ls "${PROJECT_ROOT}/正文/" | head -5
```

成功标准：
- `state.json` 存在且关键字段已填写
- `大纲/总纲.md` 包含用户提供的大纲内容
- 若为模式B，正文章节已正确导入
- 提示用户可以使用 `/webnovel-write {next_chapter}` 继续写作

## 失败处理

- 章节文件读取失败：记录错误，继续处理其他章节
- 编号识别失败：询问用户手动指定
- 目录创建失败：检查权限和路径

## 后续操作

导入完成后，提示用户：

1. **开始续写**：
   ```
   /webnovel-write 51   # 从第51章开始写
   ```

2. **检查上下文**：
   ```
   /webnovel-query recent   # 查看最近章节摘要
   ```
