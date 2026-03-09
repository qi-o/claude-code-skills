---
name: novel-downloader
description: |
  缃戠粶灏忚涓嬭浇涓庡悎骞跺伐鍏枫€傚綋鐢ㄦ埛闇€瑕佷笅杞界綉缁滃皬璇淬€佺埇鍙栧皬璇寸綉绔欍€佸皢鍦ㄧ嚎灏忚淇濆瓨涓烘湰鍦版枃浠舵椂浣跨敤姝ゆ妧鑳姐€?
  瑙﹀彂鍦烘櫙锛?
  (1) 鐢ㄦ埛鎻愪緵灏忚URL瑕佹眰涓嬭浇
  (2) 鐢ㄦ埛璇?涓嬭浇灏忚"銆?鐖彇灏忚"銆?淇濆瓨灏忚"
  (3) 鐢ㄦ埛鎻愬埌鍏蜂綋灏忚缃戠珯濡?alphapolis銆乻yosetu銆乲akuyomu銆乭ostboard銆佽捣鐐广€佺旱妯瓑
  (4) 鐢ㄦ埛闇€瑕佸皢澶氱珷鑺傚皬璇村悎骞朵负鍗曚釜鏂囦欢(txt/epub)
  鏀寔鐨勭綉绔欑被鍨嬶細鏃ユ湰杞诲皬璇寸珯(alphapolis, syosetu, kakuyomu)銆佷腑鏂囧皬璇寸珯銆佽嫳鏂囧皬璇寸珯銆佽嫳鏂囪鍧涚珯(hostboard, literotica)绛夈€?
  鍙嚜鍔ㄥ垎鏋愮綉绔欑粨鏋勫苟鐢熸垚鐖櫕浠ｇ爜銆?
  Do NOT use for general file downloads or video downloads (use aria2-downloader instead).
license: MIT
allowed-tools: "Bash(python:*) WebFetch Read Write"
compatibility: Requires Python with requests, beautifulsoup4, scrapegraphai
version: 0.2.0
metadata:
  category: media-tools
---

# Novel Downloader - 缃戠粶灏忚涓嬭浇鎶€鑳?

## 蹇€熷紑濮嬶細宸叉敮鎸佺綉绔?

瀵逛簬宸叉湁鑴氭湰鐨勭綉绔欙紝鐩存帴浣跨敤 `scripts/` 鐩綍涓嬬殑鑴氭湰锛?

| 缃戠珯 | 鑴氭湰 | 鐢ㄦ硶 |
|------|------|------|
| alphapolis.co.jp | `alphapolis.py` | 闇€Playwright锛屼慨鏀筓RL鍚庤繍琛?|
| novel18.syosetu.com | `syosetu_r18.py` | 淇敼URL鍚庤繍琛?|
| purple-novel.com | `purple_novel.py` | WordPress绔欙紝淇敼URL鍚庤繍琛?|
| literotica.com | `literotica.py` | 浣跨敤curl锛屼慨鏀筍ERIES_URL鍚庤繍琛?|
| hostboard.com | `hostboard.py` | 闇€DrissionPage锛屼慨鏀筓RLS鍚庤繍琛?|

```bash
# 浣跨敤鏂规硶锛氬鍒惰剼鏈埌宸ヤ綔鐩綍锛屼慨鏀筃OVEL_URL鍜孫UTPUT_FILE锛岀劧鍚庤繍琛?
python -X utf8 鑴氭湰鍚?py
```

## 鏂扮綉绔欏鐞嗘祦绋?

### 鏂瑰紡涓€锛氭櫤鑳藉垎鏋愶紙鎺ㄨ崘锛?

浣跨敤 ScrapeGraphAI + LLM 鑷姩鍒嗘瀽缃戠珯缁撴瀯锛屾棤闇€鎵嬪姩鏌ョ湅 HTML锛?

```bash
# 璁剧疆鐜鍙橀噺锛堟櫤璋?GLM锛?
set SCRAPEGRAPH_API_KEY=浣犵殑API瀵嗛挜
set SCRAPEGRAPH_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
set SCRAPEGRAPH_MODEL=GLM-4.7

# 1. 鍒嗘瀽鐩綍椤?鈫?鑾峰彇绔犺妭鍒楄〃鍜岀珯鐐逛俊鎭?
python scripts/smart_analyzer.py toc "https://example.com/novel/123"

# 2. 鍒嗘瀽绔犺妭椤?鈫?鑾峰彇姝ｆ枃閫夋嫨鍣ㄥ拰椤甸潰缁撴瀯
python scripts/smart_analyzer.py chapter "https://example.com/novel/123/chapter/1"

# 3. 鑷姩鐢熸垚鍩虹鐖櫕鑴氭湰
python scripts/smart_analyzer.py script "https://example.com/novel/123"
```

鏅鸿兘鍒嗘瀽杈撳嚭 JSON 缁撴瀯鍖栫粨鏋滐紝鍖呭惈閫夋嫨鍣ㄣ€佸弽鐖俊鎭€佺珷鑺傚垪琛ㄧ瓑銆?
Agent 鏍规嵁鍒嗘瀽缁撴灉寰皟鑴氭湰锛屽姞鍏ュ弽鐖€昏緫鍚庡嵆鍙壒閲忎笅杞姐€?

鏀寔鐨?LLM锛氭櫤璋?GLM銆丱penAI銆丟emini銆丟roq銆丱llama锛堟湰鍦板厤璐癸級绛変换浣?OpenAI 鍏煎 API銆?

### 鏂瑰紡浜岋細鎵嬪姩鍒嗘瀽锛堝閫夛級

褰撴櫤鑳藉垎鏋愬け璐ユ垨闇€瑕佺簿纭帶鍒舵椂锛?

1. 妫€鏌ユ槸鍚︽湁鐜版垚鑴氭湰
```
1. WebFetch 鑾峰彇鐩綍椤?鈫?鍒嗘瀽鏍囬/浣滆€?绔犺妭鍒楄〃缁撴瀯
2. WebFetch 鑾峰彇绔犺妭椤?鈫?鍒嗘瀽姝ｆ枃閫夋嫨鍣?鏄惁AJAX/鍙嶇埇鏈哄埗
```

### 3. 缃戠珯妯″紡璇嗗埆

| 妯″紡 | 鐗瑰緛 | 澶勭悊鏂瑰紡 |
|------|------|----------|
| 闈欐€?| 姝ｆ枃鍦℉TML涓?| 鐩存帴BeautifulSoup瑙ｆ瀽 |
| AJAX | 姝ｆ枃閫氳繃JS鍔犺浇 | 鍒嗘瀽API绔偣锛屾ā鎷熻姹?|
| WAF淇濇姢 | 杩斿洖202/403 | 浣跨敤Playwright娴忚鍣ㄨ嚜鍔ㄥ寲 |
| Cloudflare Turnstile | 403 + JS Challenge | 浣跨敤DrissionPage锛堢湡瀹炴祻瑙堝櫒锛?|
| 璁哄潧甯栧瓙 | 姝ｆ枃涓庤瘎璁烘贩鍚?| 鎸夊唴瀹归暱搴﹁繃婊わ紙>1000瀛楃涓烘鏂囷級 |
| 鍙嶇埇 | 闇€token/CSRF | 姣忕珷鏂皊ession + 鎼哄甫token |
| 骞撮緞楠岃瘉 | 闇€瑕乧ookie | 璁剧疆楠岃瘉cookie |

### 4. 鍏抽敭浠ｇ爜妯″紡

#### WAF淇濇姢缃戠珯 (濡傛柊鐗坅lphapolis)
```python
from playwright.sync_api import sync_playwright
# 闇€瑕? pip install scrapling[all] && scrapling install

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    html = page.content()
    # 瑙ｆ瀽html...
```

#### CSRF淇濇姢缃戠珯
```python
# 姣忕珷浣跨敤鐙珛session
new_session = requests.Session()
resp = new_session.get(chapter_url)
token = re.search(r"'token':\s*'([a-f0-9]+)'", resp.text).group(1)
xsrf = urllib.parse.unquote(new_session.cookies.get('XSRF-TOKEN', ''))
body = new_session.post(api_url, data={...}, headers={'X-XSRF-TOKEN': xsrf})
```

#### Cloudflare Turnstile 淇濇姢缃戠珯 (濡俬ostboard.com)
```python
from DrissionPage import ChromiumPage, ChromiumOptions
# 闇€瑕? pip install DrissionPage

co = ChromiumOptions()
co.set_argument('--no-sandbox')
page = ChromiumPage(co)
page.get(url)
# 绛夊緟楠岃瘉閫氳繃锛堢害10-20绉掞級锛屾娴嬫爣棰樺彉鍖栧拰椤甸潰闀垮害
html = page.html
# 瑙ｆ瀽html...
```

#### 璁哄潧甯栧瓙鍐呭杩囨护
```python
# 閫氳繃鍐呭闀垮害鍖哄垎姝ｆ枃鍜岃瘎璁?
post_msgs = soup.find_all(id=re.compile(r'post_message_'))
story_parts = [msg.get_text('\n', strip=True) for msg in post_msgs
               if len(msg.get_text()) >= 1000]  # >1000瀛楃涓烘鏂?
```

#### 骞撮緞楠岃瘉缃戠珯 (濡俷ovel18.syosetu.com)
```python
session.cookies.set('over18', 'yes', domain='.syosetu.com')
```

## 甯歌闂閫熸煡

| 闂 | 鍘熷洜 | 瑙ｅ喅 |
|------|------|------|
| 202鐘舵€佺爜 | AWS WAF | 浣跨敤Playwright |
| 鍐呭涓虹┖ | AJAX鍔犺浇 | 鎵続PI绔偣 |
| 419閿欒 | CSRF | 鍔燲-XSRF-TOKEN |
| 鍓峃绔犵┖ | Session姹℃煋 | 姣忕珷鏂皊ession |
| 涔辩爜 | 缂栫爜閿欒 | resp.encoding='utf-8' |
| 閲嶅畾鍚?| 骞撮緞楠岃瘉 | 璁剧疆cookie |
| HTTP/2鍗忚閿欒 | requests/playwright涓嶅吋瀹?| 浣跨敤curl subprocess |
| Cloudflare Turnstile 403 | Cloudflare JS楠岃瘉 | 浣跨敤DrissionPage |
| 璁哄潧璇勮娣峰叆 | 姝ｆ枃涓庤瘎璁哄湪鍚屼竴椤?| 鎸夊唴瀹归暱搴﹁繃婊?|

## 宸茬煡缃戠珯閰嶇疆

璇﹁ `references/sites/` 鐩綍銆?

## 渚濊禆

```bash
pip install requests beautifulsoup4
# 鏅鸿兘鍒嗘瀽锛堟柊绔欑偣鑷姩璇嗗埆锛?
pip install scrapegraphai
# WAF淇濇姢缃戠珯闇€瑕?
pip install scrapling[all] && scrapling install
# Cloudflare Turnstile 淇濇姢缃戠珯闇€瑕?
pip install DrissionPage
```

## 浠诲姟瀹屾垚鍚?

涓嬭浇瀹屾垚鍚庯紝璋冪敤 `/skill-evolution-manager` 杩涜澶嶇洏锛屽皢鏂板彂鐜扮殑闂鍜岃В鍐虫柟妗堝浐鍖栧埌鎶€鑳戒腑銆?

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
- Scrapling 集成应使用 try/except 包裹所有导入，不可用时自动 fallback 到 requests/curl，保持向后兼容

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
- scrapling 0.4 中 PlayWrightFetcher 已改名为 DynamicFetcher，import 时需用 DynamicFetcher
- scrapling 0.4 Response 对象属性 .html 已改为 .html_content，.content 已改为 .body
- scrapling 单独 pip install scrapling 不够，需要 pip install scrapling[all] 才能获得 browserforge 和 patchright 等依赖
- scrapling Fetcher(auto_match=False) 构造参数已废弃，应改用 Fetcher.configure(auto_match=False)
- scrapling 正确导入方式：from scrapling.fetchers import Fetcher, DynamicFetcher, StealthyFetcher