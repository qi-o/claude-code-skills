---
name: webnovel-continue
description: |
  简化版续写命令。从指定章节或最新章节+1开始写作，是 /webnovel-write 的快捷入口，支持自动检测起始章节。
  触发场景：
  (1) 用户说"续写"、"继续写"、"写下一章"、"接着写"、"/webnovel-continue"
  (2) 用户想从当前进度继续写作，无需手动指定章节号
  与 webnovel-write 的区别：自动检测最新章节+1，无需明确指定章节号。
  Do NOT use for project initialization (use webnovel-init instead).
allowed-tools: Read Write Edit Grep Bash Task
---

# Continue Writing (简化续写模块)

## 目标

- 提供一个简化版的续写命令
- 支持从指定章节号开始写作
- 自动检测起始章节（最新章+1）

## 使用方式

```
/webnovel-continue           # 从最新章节+1开始写
/webnovel-continue 50        # 从第50章开始写
/webnovel-continue latest    # 同上，从最新章节+1开始写
/webnovel-continue next      # 同上，从最新章节+1开始写
```

## 执行流程

### 1. 确定起始章节

根据参数确定要写的章节号：

| 参数 | 行为 |
|------|------|
| 无参数 | 自动查找最新章节，+1 |
| 数字 N | 从第 N 章开始写 |
| `latest` / `next` | 从最新章节+1开始写 |

### 2. 检测项目

确认当前工作目录下有可用的网文项目：

```bash
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"
export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

### 3. 检测起始章节

查询已有章节：

```bash
# 列出所有正文章节
ls "${PROJECT_ROOT}/正文/" | sort -V

# 或从 state.json 读取当前进度
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" state get-progress
```

### 4. 执笔写作

确定章节号后，调用 `/webnovel-write`：

```bash
# 例如确定要写第 15 章
/webnovel-write 15
```

## 实现逻辑

### 自动检测最新章节

1. 扫描 `正文/` 目录
2. 提取章节编号（正则匹配 `第(\d+)章`）
3. 取最大编号 + 1

```python
import re
from pathlib import Path

def get_next_chapter(project_root: str) -> int:
    """检测下一个章节号"""
    content_dir = Path(project_root) / "正文"
    if not content_dir.exists():
        return 1

    max_num = 0
    pattern = re.compile(r"第(\d+)章")

    for f in content_dir.glob("*.md"):
        match = pattern.search(f.stem)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    return max_num + 1
```

### 参数解析

| 输入 | 解析结果 |
|------|----------|
| `/webnovel-continue` | next_chapter = auto_detect() |
| `/webnovel-continue 5` | next_chapter = 5 |
| `/webnovel-continue 10` | next_chapter = 10 |
| `/webnovel-continue latest` | next_chapter = auto_detect() |
| `/webnovel-continue next` | next_chapter = auto_detect() |

## 错误处理

| 错误 | 处理 |
|------|------|
| 无项目 | 提示先用 `/webnovel-import` 或 `/webnovel-init` |
| 目录不存在 | 创建 `正文/` 目录 |
| 章节文件已存在 | 询问是否覆盖或跳过 |

## 示例对话

### 示例1：自动检测

```
用户: /webnovel-continue
系统: 检测到最新章节为第12章，将从第13章开始写作。
→ 调用 /webnovel-write 13
```

### 示例2：指定章节

```
用户: /webnovel-continue 50
系统: 确认从第50章开始写作。
→ 调用 /webnovel-write 50
```

### 示例3：无项目

```
用户: /webnovel-continue
错误: 未检测到网文项目。
提示: 请先使用 /webnovel-import 导入已有小说，或使用 /webnovel-init 创建新项目。
```

## 与 webnovel-write 的关系

`/webnovel-continue` 是 `/webnovel-write` 的简化入口：

- **相同点**：最终都调用相同的写作流程
- **不同点**：
  - `webnovel-write` 需要明确指定章节号
  - `webnovel-continue` 支持自动检测起始章节

## 验证

成功标准：
- 正确解析用户输入的章节号
- 正确检测最新章节（当参数为空时）
- 成功调用 `/webnovel-write` 开始写作
