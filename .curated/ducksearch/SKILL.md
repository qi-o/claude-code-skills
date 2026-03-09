---
name: ducksearch
description: 浣跨敤 DuckDuckGo 杩涜缃戦〉鎼滅储鍜屽唴瀹规彁鍙栫殑鍛戒护琛屽伐鍏枫€傚綋鐢ㄦ埛闇€瑕佹悳绱㈢綉缁滀俊鎭€佹煡鎵捐祫鏂欍€佽幏鍙栫綉椤靛唴瀹规椂浣跨敤姝?skill銆傝Е鍙戝満鏅寘鎷細(1) 鎼滅储缃戠粶鍐呭 (2) 鑾峰彇缃戦〉鏂囨湰 (3) 浣跨敤 DuckDuckGo 鎼滅储 (4) 鎶撳彇缃戦〉鍐呭 (5) 閰嶇疆 MCP 鎼滅储鏈嶅姟鍣?(6) reddit 鎼滅储 (7) 绀惧尯璁ㄨ (8) r/bioinformatics銆俇se when user says "鎼滀竴涓?, "DuckDuckGo", "duck鎼滅储", "缃戦〉鎼滅储", "search the web", "reddit", "绀惧尯璁ㄨ", or "r/bioinformatics". Do NOT use for deep research reports (use deep-research) or Gemini-based research (use web-research). 鐢卞井淇″叕浼楀彿銆屽瓧鑺傜瑪璁版湰銆嶆彁渚涖€?
license: MIT
version: 1.0.0
metadata:
  category: research-knowledge
---

# ducksearch

缃戦〉鎼滅储鍜屽唴瀹规彁鍙栧伐鍏凤紝鐢卞井淇″叕浼楀彿銆屽瓧鑺傜瑪璁版湰銆嶆彁渚涖€?

## 蹇€熶娇鐢?

### 鎼滅储缃戠粶

```bash
npx -y ducksearch search "鎼滅储鍏抽敭璇?
npx -y ducksearch search "Claude AI" -n 5      # 闄愬埗缁撴灉鏁伴噺
npx -y ducksearch search "Claude AI" -o        # 鑷姩鎵撳紑绗竴涓粨鏋?
```

### 鑾峰彇缃戦〉鍐呭

```bash
npx -y ducksearch fetch https://example.com
npx -y ducksearch fetch https://example.com --raw      # 鍘熷 HTML
npx -y ducksearch fetch https://example.com -o out.txt # 淇濆瓨鍒版枃浠?
npx -y ducksearch fetch https://example.com --json     # JSON 鏍煎紡
```

## 鍦烘櫙 4: Reddit 鎼滅储

### Reddit 鎼滅储锛坴ia DuckDuckGo site 闄愬畾锛?

閫傚悎鏌ユ壘绀惧尯璁ㄨ銆佺粡楠屽垎浜€佸伐鍏锋帹鑽愩€傛棤闇€ API key锛岀洿鎺ュ彲鐢ㄣ€?

**鏂规硶 1锛氱洿鎺ョ敤 Python 鑴氭湰锛堟帹鑽愶級**

```bash
python ~/.claude/skills/.curated/ducksearch/scripts/reddit_search.py "鍏抽敭璇? --max 10
python ~/.claude/skills/.curated/ducksearch/scripts/reddit_search.py "scRNA-seq pipeline" --subreddit bioinformatics
python ~/.claude/skills/.curated/ducksearch/scripts/reddit_search.py "best tools" --output json
```

**鏂规硶 2锛氱敤 DuckDuckGo 闄愬畾 Reddit**

```bash
npx -y ducksearch search "site:reddit.com/r/bioinformatics scRNA-seq"
npx -y ducksearch search "site:reddit.com 鍏抽敭璇?
```

**甯哥敤鐢熺墿淇℃伅瀛?subreddit锛?*
- r/bioinformatics
- r/MachineLearning
- r/learnbioinformatics
- r/genomics
- r/statistics

## MCP 鏈嶅姟鍣ㄩ厤缃?

鍦?Claude Code 涓娇鐢?ducksearch 浣滀负 MCP 鏈嶅姟鍣細

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

### MCP 宸ュ叿

- **DuckDuckGoWebSearch**: 鎼滅储缃戠粶鍐呭锛岃繑鍥炴爣棰樸€侀摼鎺ャ€佹憳瑕?
- **UrlContentExtractor**: 鎻愬彇缃戦〉绾枃鏈唴瀹?

## 鍏ㄥ眬瀹夎锛堝彲閫夛級

```bash
npm install -g ducksearch
ducksearch search "鍏抽敭璇?
ducksearch fetch https://example.com
```

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- ducksearch 增强层脚本位于 scripts/scrapling_fetch.py，支持 --mode static|browser|stealth|auto 和 --json 输出
- 中国考研/教育类信息优先使用研招网官方源(yz.chsi.com.cn)，比新闻网站更稳定

### Known Fixes & Workarounds
- scrapling 0.4 中 PlayWrightFetcher 已改名为 DynamicFetcher
- scrapling 0.4 Response 对象属性 .html → .html_content，.content → .body
- scrapling 需要 pip install scrapling[all] 才能获得完整依赖
- scrapling_fetch.py 的 auto 模式升级链：Fetcher → DynamicFetcher → StealthyFetcher
- 考研国家线历史数据URL模式: yz.chsi.com.cn/kyzx/zt/lnfsx{年份}.shtml (如2025年是lnfsx2025.shtml)
- 研招网首页有"近五年研考分数线及趋势图"入口，包含历年分数线汇总
- 网络搜索失败时，直接用Python requests访问官方页面更可靠
- DuckDuckGo HTML搜索会被CAPTCHA拦截，无法解析结果