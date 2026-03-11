---
name: novel-downloader
description: |
  网络小说下载与合并工具。当用户需要下载网络小说、爬取小说网站、将在线小说保存为本地文件时使用此技能。
  触发场景：
  (1) 用户提供小说URL要求下载
  (2) 用户说"下载小说"、"爬取小说"、"保存小说"
  (3) 用户提到具体小说网站如 alphapolis、syosetu、kakuyomu、hostboard、起点、纵横等
  (4) 用户需要将多章节小说合并为单个文件(txt/epub)
  支持的网站类型：日本轻小说站(alphapolis, syosetu, kakuyomu)、中文小说站、英文小说站、英文论坛站(hostboard, literotica)等。
  可自动分析网站结构并生成爬虫代码。
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

### User Preferences
- 下载的小说文件必须以小说标题命名（如「タイトル.txt」），不要使用小说ID或编号命名
- ScrapeGraphAI 智能分析优先用于 chapter 模式（识别选择器最可靠），toc 模式用于结构分析而非全量章节提取
- LLM 只在侦察阶段调用（分析新站点结构），批量下载仍用传统 requests/Playwright/DrissionPage
- 智谱 GLM-4.7 作为默认 LLM，通过 OpenAI 兼容端点调用
- Steel Browser 暂不引入，DrissionPage + Playwright 已覆盖现有反爬需求
- HostBoard 下载优先使用 printthread.php?t=THREAD_ID 格式的打印版本 URL
- 打印版本将所有帖子合并到单页，无需分页处理
- DrissionPage 必须使用 headless(False) 才能通过 Cloudflare Turnstile 验证

### Known Fixes & Workarounds
- literotica.com 使用 SPA 架构但内容在服务端渲染的 HTML 中
- requests 和 Playwright 遇到 HTTP/2 协议错误时，使用 curl subprocess 绕过
- literotica 正文选择器为 div[class*=_article__content]，不要使用 div.panel.article
- literotica 章节内分页检测应查找下一页链接 a[href*=?page=N] 而非文本匹配
- hostboard.com 使用 Cloudflare Turnstile 保护，requests/curl/cloudscraper/curl_cffi/Playwright(含stealth) 均无法绕过
- Cloudflare Turnstile 唯一有效方案是 DrissionPage（基于 CDP 协议控制真实浏览器）
- hostboard.com 是 vBulletin 论坛，帖子内容选择器为 [id^=post_message_]
- 论坛小说提取策略：按内容长度过滤（>1000字符为正文，<1000字符为评论）
- DrissionPage 批量下载时复用同一浏览器实例，首次通过 Cloudflare 后后续请求无需再等
- Cloudflare 验证通常需要 10-20 秒，通过检测页面标题变化和长度判断是否通过
- ScrapeGraphAI 1.73.0 的 model_tokens 参数不能放在 llm 配置中（会被传给 OpenAI API 报错），也不能放在顶层（会被忽略），当前默认 8192 tokens
- 8192 token 限制导致大页面（如200+章节目录）内容被截断，LLM 无法提取完整章节列表，因此 toc 模式改为分析结构而非提取全量数据
- Windows 下设置环境变量运行 smart_analyzer.py 需要用 Python wrapper（importlib）或 cmd /C，bash 的 set X=Y && 语法不生效
- ScrapeGraphAI 在 Python 3.14 下有 Pydantic V1 兼容性警告但不影响功能
- 智谱 GLM OpenAI 兼容端点为 https://open.bigmodel.cn/api/paas/v4/，不是 Anthropic 兼容端点
- chapter 分析模式比 toc 模式更可靠，单章页面内容通常在 8192 token 限制内
- ScrapeGraphAI 内部会打印 dict 结果到 stdout，脚本输出会包含重复内容（一次 dict 一次 JSON）
- Cloudflare 检测逻辑：只检查标题是否含 "请稍候" 或 "Just a moment"，不要检查 HTML 内容中的 challenge-platform（会误判已加载页面）
- HostBoard 打印版本内容选择器：div.content > blockquote.restore，而非 post_message_ ID 选择器
- 成功加载判断：html_len > 50000 且标题不含 "请稍候" 即认为通过验证