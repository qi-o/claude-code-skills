---
name: novel-downloader
description: >
  网络小说下载与合并工具。当用户需要下载网络小说、爬取小说网站、将在线小说保存为本地文件时使用此技能。
  触发场景：
  (1) 用户提供小说URL要求下载
  (2) 用户说"下载小说"、"爬取小说"、"保存小说"
  (3) 用户提到具体小说网站如 alphapolis、syosetu、kakuyomu、hostboard、起点、纵横等
  (4) 用户需要将多章节小说合并为单个文件(txt/epub)
  支持的网站类型：日本轻小说站(alphapolis, syosetu, kakuyomu)、中文小说站、英文小说站、英文论坛站(hostboard, literotica)等。
  可自动分析网站结构并生成爬虫代码。
  Triggers (EN): download novel, web novel download, scrape fiction, light novel download, save web fiction,
  novel scraper, merge chapters to epub, alphapolis download, syosetu download, kakuyomu download.
  Do NOT use for general file downloads or video downloads (use aria2-downloader instead).
license: MIT
allowed-tools: "Bash(python:*) WebFetch Read Write"
compatibility: Requires Python with requests, beautifulsoup4, scrapegraphai
version: 0.2.0
metadata:
  category: media-tools
---

# Novel Downloader - 网络小说下载技能

## 快速开始：已支持网站

对于已有脚本的网站，直接使用 `scripts/` 目录下的脚本：

| 网站 | 脚本 | 用法 |
|------|------|------|
| alphapolis.co.jp | `alphapolis.py` | 需Playwright，修改URL后运行 |
| novel18.syosetu.com | `syosetu_r18.py` | 修改URL后运行 |
| purple-novel.com | `purple_novel.py` | WordPress站，修改URL后运行 |
| literotica.com | `literotica.py` | 使用curl，修改SERIES_URL后运行 |
| hostboard.com | `hostboard.py` | 需DrissionPage，修改URLS后运行 |

```bash
# 使用方法：复制脚本到工作目录，修改NOVEL_URL和OUTPUT_FILE，然后运行
python -X utf8 脚本名.py
```

## 新网站处理流程

### 方式一：智能分析（推荐）

使用 ScrapeGraphAI + LLM 自动分析网站结构，无需手动查看 HTML：

```bash
# 设置环境变量（智谱 GLM）
set SCRAPEGRAPH_API_KEY=你的API密钥
set SCRAPEGRAPH_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
set SCRAPEGRAPH_MODEL=GLM-4.7

# 1. 分析目录页 → 获取章节列表和站点信息
python scripts/smart_analyzer.py toc "https://example.com/novel/123"

# 2. 分析章节页 → 获取正文选择器和页面结构
python scripts/smart_analyzer.py chapter "https://example.com/novel/123/chapter/1"

# 3. 自动生成基础爬虫脚本
python scripts/smart_analyzer.py script "https://example.com/novel/123"
```

智能分析输出 JSON 结构化结果，包含选择器、反爬信息、章节列表等。
Agent 根据分析结果微调脚本，加入反爬逻辑后即可批量下载。

支持的 LLM：智谱 GLM、OpenAI、Gemini、Groq、Ollama（本地免费）等任何 OpenAI 兼容 API。

### 方式二：手动分析（备选）

当智能分析失败或需要精确控制时：

1. 检查是否有现成脚本
```
1. WebFetch 获取目录页 → 分析标题/作者/章节列表结构
2. WebFetch 获取章节页 → 分析正文选择器/是否AJAX/反爬机制
```

### 3. 网站模式识别

| 模式 | 特征 | 处理方式 |
|------|------|----------|
| 静态 | 正文在HTML中 | 直接BeautifulSoup解析 |
| AJAX | 正文通过JS加载 | 分析API端点，模拟请求 |
| WAF保护 | 返回202/403 | 使用Playwright浏览器自动化 |
| Cloudflare Turnstile | 403 + JS Challenge | 使用DrissionPage（真实浏览器） |
| 论坛帖子 | 正文与评论混合 | 按内容长度过滤（>1000字符为正文） |
| 反爬 | 需token/CSRF | 每章新session + 携带token |
| 年龄验证 | 需要cookie | 设置验证cookie |

### 4. 关键代码模式

#### WAF保护网站 (如新版alphapolis)
```python
from playwright.sync_api import sync_playwright
# 需要: pip install playwright && playwright install chromium

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    html = page.content()
    # 解析html...
```

#### CSRF保护网站
```python
# 每章使用独立session
new_session = requests.Session()
resp = new_session.get(chapter_url)
token = re.search(r"'token':\s*'([a-f0-9]+)'", resp.text).group(1)
xsrf = urllib.parse.unquote(new_session.cookies.get('XSRF-TOKEN', ''))
body = new_session.post(api_url, data={...}, headers={'X-XSRF-TOKEN': xsrf})
```

#### Cloudflare Turnstile 保护网站 (如hostboard.com)
```python
from DrissionPage import ChromiumPage, ChromiumOptions
# 需要: pip install DrissionPage

co = ChromiumOptions()
co.set_argument('--no-sandbox')
page = ChromiumPage(co)
page.get(url)
# 等待验证通过（约10-20秒），检测标题变化和页面长度
html = page.html
# 解析html...
```

#### 论坛帖子内容过滤
```python
# 通过内容长度区分正文和评论
post_msgs = soup.find_all(id=re.compile(r'post_message_'))
story_parts = [msg.get_text('\n', strip=True) for msg in post_msgs
               if len(msg.get_text()) >= 1000]  # >1000字符为正文
```

#### 年龄验证网站 (如novel18.syosetu.com)
```python
session.cookies.set('over18', 'yes', domain='.syosetu.com')
```

## 常见问题速查

| 问题 | 原因 | 解决 |
|------|------|------|
| 202状态码 | AWS WAF | 使用Playwright |
| 内容为空 | AJAX加载 | 找API端点 |
| 419错误 | CSRF | 加X-XSRF-TOKEN |
| 前N章空 | Session污染 | 每章新session |
| 乱码 | 编码错误 | resp.encoding='utf-8' |
| 重定向 | 年龄验证 | 设置cookie |
| HTTP/2协议错误 | requests/playwright不兼容 | 使用curl subprocess |
| Cloudflare Turnstile 403 | Cloudflare JS验证 | 使用DrissionPage |
| 论坛评论混入 | 正文与评论在同一页 | 按内容长度过滤 |

## 已知网站配置

详见 `references/sites/` 目录。

## 依赖

```bash
pip install requests beautifulsoup4
# 智能分析（新站点自动识别）:
pip install scrapegraphai
# WAF保护网站需要:
pip install playwright && playwright install chromium
# Cloudflare Turnstile 保护网站需要:
pip install DrissionPage
```

## 任务完成后

下载完成后，调用 `/skill-evolution-manager` 进行复盘，将新发现的问题和解决方案固化到技能中。

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### Known Fixes & Workarounds
- literotica.com 使用 SPA 架构但内容在服务端渲染的 HTML 中
- requests 和 Playwright 遇到 HTTP/2 协议错误时，使用 curl subprocess 绕过
- literotica 正文选择器为 div[class*=_article__content]，不要使用 div.panel.article
- literotica 章节内分页检测应查找下一页链接 a[href*=?page=N] 而非文本匹配
- Windows 下 Clash Verge 代理出口封锁 novel18.syosetu.com，导致 SSL handshake 失败。解决：curl -x '' 绕过系统代理直连
- Python requests 会话受代理影响，即使 trust_env=False 仍可能 SSL 失败。改用 subprocess + curl -x '' subprocess 直连更可靠
- novel18.syosetu.com 目录页章节标题需用 href 周围文本提取，不能只靠选择器

### Custom Instruction Injection

遇到 HTTP/2 协议错误时，优先尝试 curl 而非切换浏览器自动化工具