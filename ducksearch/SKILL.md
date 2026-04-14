---
name: ducksearch
description: 使用 DuckDuckGo 进行网页搜索和内容提取的命令行工具。当用户需要搜索网络信息、查找资料、获取网页内容时使用此 skill。触发场景包括：(1) 搜索网络内容 (2) 获取网页文本 (3) 使用 DuckDuckGo 搜索 (4) 抓取网页内容 (5) 配置 MCP 搜索服务器。Use when user says "搜一下", "DuckDuckGo", "duck搜索", "网页搜索", or "search the web". Do NOT use for deep research reports (use deep-research) or Gemini-based research (use web-research). 由微信公众号「字节笔记本」提供。
license: MIT
version: 1.0.0
metadata:
  category: research-knowledge
---

# ducksearch

网页搜索和内容提取工具，由微信公众号「字节笔记本」提供。

## 快速使用

### 搜索网络

```bash
npx -y ducksearch search "搜索关键词"
npx -y ducksearch search "Claude AI" -n 5      # 限制结果数量
npx -y ducksearch search "Claude AI" -o        # 自动打开第一个结果
```

### 获取网页内容

```bash
npx -y ducksearch fetch https://example.com
npx -y ducksearch fetch https://example.com --raw      # 原始 HTML
npx -y ducksearch fetch https://example.com -o out.txt # 保存到文件
npx -y ducksearch fetch https://example.com --json     # JSON 格式
```

## MCP 服务器配置

在 Claude Code 中使用 ducksearch 作为 MCP 服务器：

```json
{
  "mcpServers": {
    "ducksearch": {
      "command": "npx",
      "args": ["-y", "ducksearch", "mcp"]
    }
  }
}
```

### MCP 工具

- **DuckDuckGoWebSearch**: 搜索网络内容，返回标题、链接、摘要
- **UrlContentExtractor**: 提取网页纯文本内容

## 全局安装（可选）

```bash
npm install -g ducksearch
ducksearch search "关键词"
ducksearch fetch https://example.com
```

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 自动打开浏览器 | 使用 `-o` 参数时 | 确认是否在默认浏览器中打开搜索结果 |
| 保存到文件 | 使用 `-o out.txt` 输出到指定路径 | 确认输出路径和是否覆盖已有文件 |
| 全局安装 | 执行 `npm install -g ducksearch` | 确认用户同意全局安装 npm 包 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| npx 执行失败 | 命令返回非零退出码或超时 | 检查 Node.js/npm 是否可用，建议用户全局安装 `npm install -g ducksearch` |
| 搜索无结果 | 返回空结果列表 | 缩小关键词范围或换用同义词重试，提示用户尝试 `deep-research` 或 `web-research` |
| 网页抓取失败 | fetch 返回空内容或超时 | 检查 URL 可访问性，尝试 `--raw` 模式或使用 `web_reader` MCP 工具替代 |
| MCP 服务器启动失败 | Claude Code 报错连接 ducksearch MCP | 验证 settings.json 中 MCP 配置语法，检查 npx 可用性 |

**原则**：不要静默失败——报错时同时提供修复建议。
