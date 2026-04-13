---
name: webnovel-continue
description: |
  简化版续写命令。自动检测下一章节并调用 InkOS 完整流水线写作。
  触发场景：
  (1) 用户说"续写"、"继续写"、"写下一章"、"接着写"、"/webnovel-continue"
  (2) 用户想从当前进度继续写作，无需手动指定章节号
  与 webnovel-write 的区别：自动检测最新章节+1，无需明确指定章节号。
  Do NOT use for project initialization (use webnovel-init instead).
allowed-tools: Read Write Edit Grep Bash Task
---

# Continue Writing (InkOS 集成版)

## 目标

- 自动检测下一个章节号
- 调用 InkOS 完整写作流水线 (`inkos write next`)

## 前置条件

- InkOS 项目已初始化（存在 `inkos.json` 或 `books/` 目录）
- 项目位于 InkOS 工作目录（默认 `E:\inkos-master`）

## 使用方式

```
/webnovel-continue           # 从最新章节+1开始写
/webnovel-continue 50        # 从第50章开始写
/webnovel-continue latest    # 从最新章节+1开始写
/webnovel-continue next      # 从最新章节+1开始写
```

## 执行流程

### 1. 确定起始章节

| 参数 | 行为 |
|------|------|
| 无参数 | 自动检测最新章节，+1 |
| 数字 N | 从第 N 章开始写 |
| `latest` / `next` | 从最新章节+1开始写 |

### 2. 检测项目与章节

使用 InkOS CLI 获取项目状态：

```bash
# 列出所有书籍
inkos book list

# 获取指定书籍的状态（含当前章节数）
inkos status <book-id>
```

自动检测逻辑：
- 从 `inkos status` 输出中读取 `currentChapter` 字段
- 若无章节，下一章为 1
- 若有章节，下一章为 currentChapter + 1

### 3. 调用 InkOS 写作

```bash
# 调用完整写作流水线（10-agent pipeline）
inkos write next <book-id>
```

InkOS 自动执行：
- **Planner**: 规划章节意图（目标、冲突、strand directive、chapter contract）
- **Composer**: 组装运行时上下文包
- **Writer**: 起草章节正文
- **Normalizer**: 长度规范化
- **Auditor**: 37+维度审查（含 anti-trope、contract compliance）
- **Reviser**: 按审查结果修订
- **State Validator**: 验证 Truth Files 一致性

若启用 webnovelCraft（strand-weave + anti-trope），Planner 会自动计算：
- Strand Weave 比例（Quest/Fire/Constellation）
- Chapter Contract（hookType、openingType、coolPointPattern、emotionalArc 差异化）
- Anti-trope 合规检查

### 4. HIL 审核（如触发）

InkOS 内置 HIL gate 会在以下条件暂停：
- FORCE：P1 审查失败、anti-AI 失败、维度 < 70
- SUGGEST：首章、卷末章

暂停时展示审核报告，等待用户决策。

## 与 webnovel-write 的关系

`/webnovel-continue` 和 `/webnovel-write` 都调用同一个 InkOS 写作流水线。
区别仅在入口参数：
- `webnovel-write` 需要明确指定章节号
- `webnovel-continue` 自动检测起始章节

## 错误处理

| 错误 | 处理 |
|------|------|
| 无 InkOS 项目 | 提示先用 `/webnovel-init` 创建项目 |
| book-id 不存在 | 提示可用的 book-id 列表 |
| 章节已存在 | 询问是否覆盖或跳过 |
