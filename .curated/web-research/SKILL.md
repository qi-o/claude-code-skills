---
name: web-research
description: 使用 gemini-search 代理进行网络内容、文档和最佳实践的研究，以实现高效的令牌搜索和缓存。当您需要获取文档、研究最佳实践或从网络收集信息时使用。 Do NOT use for DuckDuckGo-specific searches (use ducksearch) or deep research reports (use deep-research).
allowed-tools: Task, Read, Write
version: 1.0.0
metadata:
  category: research-knowledge
---

# 使用 Gemini Search 进行网络研究

此技能通过 gemini-search 代理实现高效的网络研究，该代理提供上下文隔离，节省 30-40% 的令牌，并包括内置缓存以避免冗余搜索。

## 何时使用此技能

当您需要时，请调用此技能：
- 从官方来源研究文档
- 收集最佳实践和示例
- 查找有关工具、库或框架的最新信息
- 研究 GitHub 工作流程、CI/CD 模式
- 查找 API 文档
- 查找代码模式示例
- 研究安全最佳实践
- 收集有关错误消息或问题的信息

## 工作原理

此技能使用 **gemini-search 代理**（在此插件中可用），其功能包括：
- 在隔离上下文中执行网络搜索（节省 30-40% 的令牌）
- 结果缓存 1 小时（可通过 `GEMINI_SEARCH_CACHE_TTL` 配置）
- 跟踪分析（缓存命中、查询模式、令牌节省）
- 提供结构化、相关的结果

## 研究模式

### 1. 文档研究

当您需要研究官方文档时：

```
使用 Task 工具，subagent_type="gemini-search:gemini-search" 搜索：
- "Claude Code skills documentation"
- "GitHub Actions workflow syntax"
- "ShellCheck best practices 2025"
- "Semantic versioning specification"
```

**代理的示例提示：**
```
在网上搜索关于 [topic] 的全面文档。重点关注：
1. 官方文档来源
2. 最佳实践和建议
3. 当前（2025）标准和模式
4. 实际示例和用例

请提供结构化摘要，包括关键点和源 URL。
```

### 2. 最佳实践研究

当研究最佳实践时：

```
使用 Task 工具，subagent_type="gemini-search:gemini-search" 搜索：
- "bash script best practices 2025"
- "GitHub Actions CI/CD best practices"
- "Claude Code plugin development patterns"
- "Release management workflow"
```

**代理的示例提示：**
```
研究 [topic] 的当前最佳实践。包括：
1. 行业标准方法
2. 常见模式和约定
3. 安全考虑
4. 性能优化建议
5. 常用工具和框架

提供可操作的建议和示例。
```

### 3. 故障排除和错误研究

当调查错误或问题时：

```
使用 Task 工具，subagent_type="gemini-search:gemini-search" 搜索：
- "ShellCheck SC2086 fix examples"
- "GitHub Actions workflow not triggering"
- "BATS test framework setup"
- "git tag push not triggering workflow"
```

**代理的示例提示：**
```
研究 [specific error or issue] 的解决方案。查找：
1. 此问题的常见原因
2. 推荐的解决方案和变通方法
3. 相关文档
4. 工作示例

关注来自官方文档和信誉良好来源的验证解决方案。
```

### 4. 工具和框架研究

当了解工具或框架时：

```
使用 Task 工具，subagent_type="gemini-search:gemini-search" 搜索：
- "Gemini CLI features and capabilities"
- "jq JSON processing examples"
- "GitHub CLI pr commands"
- "Trivy security scanner configuration"
```

**代理的示例提示：**
```
研究 [tool/framework name]。提供：
1. 概述和关键特性
2. 安装方法
3. 常见用例和示例
4. 配置选项
5. 与其他工具的集成

包括实际示例和当前版本信息。
```

### 5. 比较研究

当比较方法或工具时：

```
使用 Task 工具，subagent_type="gemini-search:gemini-search" 搜索：
- "GitHub Actions vs GitLab CI comparison"
- "bash vs python for shell scripts"
- "different JSON validation tools"
- "release automation strategies"
```

**代理的示例提示：**
```
比较 [option A] 与 [option B] 在 [use case] 中的表现。包括：
1. 关键差异和权衡
2. 性能考虑
3. 用例推荐
4. 社区采用和支持
5. 集成能力

提供客观比较和用例推荐。
```

## 使用说明

### 基本研究模式

**步骤 1：** 通过 Task 工具调用 gemini-search 代理

```
使用 Task 工具，参数为：
- subagent_type: "gemini-search:gemini-search"
- description: "Research [topic]"
- prompt: "[Detailed research request as shown in patterns above]"
```

**步骤 2：** 处理结果

代理将返回结构化结果，包括：
- 发现摘要
- 关键点和建议
- 参考的源 URL
- 相关示例或代码片段

**步骤 3：** 应用研究结果

使用研究结果来：
- 用当前信息回答用户问题
- 根据最佳实践实现功能
- 使用验证解决方案排除问题
- 做出明智的技术决策

### 高级用法

**多查询研究：**

当您需要研究多个相关主题时，多次调用代理并使用不同的查询：

```
1. 搜索一般概述/文档
2. 搜索具体最佳实践
3. 搜索示例和用例
4. 搜索故障排除和常见问题
```

**针对性文档搜索：**

对于官方文档，在查询中包含源约束：

```
"Claude Code skills documentation site:docs.claude.com"
"GitHub Actions workflow syntax site:docs.github.com"
"ShellCheck documentation site:shellcheck.net"
```

## 令牌效率

### 为什么这可以节省令牌

**上下文隔离：**
- 代理在隔离上下文中运行
- 仅将最终结果返回给主对话
- 不在主上下文中包含中间搜索结果
- 在研究密集型任务中节省 30-40% 的令牌

**缓存：**
- 结果缓存 1 小时（默认）
- 重复查询使用缓存（无额外 API 调用）
- 在分析中跟踪缓存命中率

**结构化输出：**
- 代理简洁地格式化结果
- 删除冗余信息
- 专注于可操作内容

### 监控令牌节省

检查分析以查看令牌节省情况：

```bash
/gemini-search:search-stats
```

这将显示：
- 执行的总搜索次数
- 缓存命中率
- 估计的令牌节省
- 顶部查询

## 配置

### 环境变量

控制缓存和行为：

```bash
# 缓存 TTL（秒）
export GEMINI_SEARCH_CACHE_TTL=3600  # 1 小时（默认）

# 缓存目录
export GEMINI_SEARCH_CACHE_DIR="/tmp/gemini-search-cache"

# 分析目录
export GEMINI_ANALYTICS_DIR="/tmp/gemini-analytics"

# 启用调试日志
export DEBUG=true
```

### 缓存管理

如有需要，清除缓存：

```bash
/gemini-search:clear-cache
```

这将删除所有缓存的搜索结果并重置分析。

## 最佳实践

### 1. 查询要具体

**好：**
```
"GitHub Actions workflow syntax for release automation with semantic versioning 2025"
```

**效果较差：**
```
"GitHub Actions workflow"
```

### 2. 包含上下文

在研究提示中提供上下文：

```
研究 Claude Code 插件库的 GitHub Actions 工作流最佳实践。
重点关注：
- Shell 脚本 linting (ShellCheck)
- JSON 验证
- 使用语义版本控制的发布自动化
- 安全扫描

包括当前（2025）的最佳实践和工作示例。
```

### 3. 利用缓存

对于同一主题的重复研究，依赖缓存结果以节省时间和令牌。

### 4. 验证来源

始终检查代理提供的源 URL，以确保信息来自：
- 官方文档
- 信誉良好的技术网站
- 最近的出版物（优先选择 2024-2025）

### 5. 与本地知识结合

使用网络研究来补充，而不是替代本地知识：
- 当本地文档不足时进行研究
- 验证当前最佳实践
- 查找最近的更改或更新
- 发现新工具或模式

## 示例

### 示例 1：研究 Claude Code Skills

```
Task tool parameters:
- subagent_type: "gemini-search:gemini-search"
- description: "Research Claude Code skills"
- prompt: "搜索关于 Claude Code skills 的全面文档。

  重点关注：
  1. 什么是技能以及它们如何工作
  2. 技能结构和 YAML frontmatter 格式
  3. 创建技能的最佳实践
  4. 设计良好的技能示例
  5. 与 allowed-tools 的工具访问限制

  请提供结构化摘要，包括关键点和官方文档 URL。

  包括来自 docs.claude.com 的当前信息。"
```

### 示例 2：研究 GitHub Actions 最佳实践

```
Task tool parameters:
- subagent_type: "gemini-search:gemini-search"
- description: "Research GitHub Actions CI/CD"
- prompt: "研究针对 shell 脚本项目的 GitHub Actions CI/CD 最佳实践。

  包括：
  1. 工作流结构和组织
  2. 跨平台的矩阵测试
  3. 依赖项的缓存策略
  4. 安全扫描集成
  5. 发布自动化模式

  重点关注 2025 年的最佳实践和工作示例。

  包括来自 docs.github.com 和信誉良好来源的信息。"
```

### 示例 3：故障排除 ShellCheck 问题

```
Task tool parameters:
- subagent_type: "gemini-search:gemini-search"
- description: "Research ShellCheck SC2086"
- prompt: "研究 ShellCheck 警告 SC2086：'双引号以防止全局匹配和单词拆分'。

  查找：
  1. 什么导致此警告
  2. 为什么修复它很重要
  3. 常见修复模式和示例
  4. 可以安全忽略的情况

  提供来自 shellcheck.net 和可信来源的实际示例。"
```

## 限制

### 何时不使用此技能

**不要用于：**
- 本地文件读取（使用 Read 工具）
- 代码分析（使用 Grep/Glob 工具）
- 本地仓库信息（使用 Bash 和 git 命令）
- 已在上下文中的信息
- 非常具体的代码库问题（优先使用本地搜索）

**可以使用：**
- 当前最佳实践和标准
- 上下文中不存在的官方文档
- 错误消息故障排除
- 工具比较和推荐
- 工具的最新更新或更改
- 来自更广泛社区的示例

### 速率限制

gemini-search 代理使用 Gemini API，可能会有速率限制：
- 遵守 API 限制
- 使用缓存减少 API 调用
- 如有需要，间隔多次搜索

## 与其他技能的集成

此网络研究技能补充其他技能：

**plugin-creator:**
- 研究 Claude Code 插件最佳实践
- 查找成功插件的示例
- 查找市场要求

**shell-script-quality:**
- 研究 ShellCheck 最佳实践
- 查找 BATS 测试示例
- 查找 shell 脚本模式

**github-repo-management:**
- 研究 GitHub Actions 模式
- 查找 CI/CD 最佳实践
- 查找发布自动化示例

## 故障排除

### 代理未响应

如果 gemini-search 代理未返回结果：

1. 检查 Gemini API 密钥是否已配置
2. 验证互联网连接
3. 使用 `/plugin list` 检查代理是否已安装
4. 查看 `/tmp/gemini-search-errors.log` 中的错误日志

### 结果质量差

如果结果不相关：

1. 使查询更具体
2. 在提示中包含更多上下文
3. 指定源约束（例如，site:docs.github.com）
4. 尝试不同的措辞

### 缓存问题

如果缓存导致过时结果：

1. 使用 `/gemini-search:clear-cache` 清除缓存
2. 使用 `GEMINI_SEARCH_CACHE_TTL` 调整缓存 TTL
3. 验证缓存目录权限

## 快速参考

**调用 gemini-search 代理：**
```
Task tool with subagent_type="gemini-search:gemini-search"
```

**研究模式：**
- 文档： "查找 [topic] 的官方文档"
- 最佳实践： "研究 [topic] 的最佳实践"
- 故障排除： "查找 [error/issue] 的解决方案"
- 工具： "研究 [tool] 的功能和用法"
- 比较： "比较 [A] 与 [B] 在 [use case] 中的表现"

**命令：**
- `/gemini-search:search [query]` - 直接搜索
- `/gemini-search:search-stats` - 查看分析
- `/gemini-search:clear-cache` - 清除缓存

## 资源

- **Gemini Search Agent**: `.claude/agents/gemini-search.md`
- **搜索命令**: `.claude/commands/search.md`
- **分析**: `/tmp/gemini-analytics/analytics.json`
- **缓存**: `/tmp/gemini-search-cache/`
- **日志**: `/tmp/gemini-search.log`

## 下一步

要有效使用此技能：

1. 确保配置了 Gemini API 密钥
2. 熟悉 gemini-search 代理的功能
3. 查看分析以了解使用模式
4. 根据需要调整缓存 TTL
5. 使用具体且丰富上下文的查询以获得最佳结果

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### Known Fixes & Workarounds
- WebFetch fails on Chinese government domains (.gov.cn, news.cn, chinanews.com.cn) with 'Unable to verify if domain is safe' — fallback to WebSearch for Chinese regulatory content
- When researching Chinese policy topics, use parallel WebSearch queries across multiple angles (phenomena, regulation, enforcement, academic) for comprehensive coverage