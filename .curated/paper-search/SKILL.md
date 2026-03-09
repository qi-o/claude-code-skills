---
name: paper-search
description: |
  瀛︽湳璁烘枃鎼滅储涓庝笅杞藉伐鍏枫€傛敮鎸?arXiv銆丳ubMed銆乥ioRxiv銆乵edRxiv銆丟oogle Scholar銆丼emantic Scholar銆丆rossRef銆両ACR 绛夊鏈暟鎹簱銆?
  瑙﹀彂鍦烘櫙锛?
  (1) 鐢ㄦ埛闇€瑕佹悳绱㈠鏈鏂囥€佹枃鐚?
  (2) 鐢ㄦ埛鎻愬埌 arXiv銆丳ubMed銆乥ioRxiv 绛夊鏈暟鎹簱
  (3) 鐢ㄦ埛璇?鎼滅储璁烘枃"銆?鏌ユ壘鏂囩尞"銆?涓嬭浇璁烘枃"
  (4) 鐢ㄦ埛杩涜瀛︽湳璋冪爺闇€瑕佷笓涓氭暟鎹簱鏀寔
  (5) 涓?deep-research skill 閰嶅悎浣跨敤锛屾彁渚?L1 绾у埆瀛︽湳璧勬枡
  鍩轰簬 openags/paper-search-mcp 杞崲锛屾棤闇€ MCP 閰嶇疆銆?
github_url: https://github.com/openags/paper-search-mcp
github_hash: cf2697fd04a7b7c1ced0e382ab84f0c214614f83
license: MIT
allowed-tools: "Bash(python:*) WebFetch Read Write"
version: 1.0.0
metadata:
  category: research-knowledge
---

# Paper Search - 瀛︽湳璁烘枃鎼滅储宸ュ叿

浠庡涓鏈暟鎹簱鎼滅储鍜屼笅杞借鏂囷紝鏃犻渶 MCP 閰嶇疆銆?

## 鏀寔鐨勬暟鎹簱

| 鏁版嵁搴?| 鎼滅储 | 涓嬭浇 | 璇存槑 |
|--------|------|------|------|
| **arXiv** | 鉁?| 鉁?| 棰勫嵃鏈紝鐗╃悊/鏁板/CS/AI |
| **PubMed** | 鉁?| 鉂?| 鐢熺墿鍖诲鏂囩尞 |
| **bioRxiv** | 鉁?| 鉁?| 鐢熺墿瀛﹂鍗版湰 |
| **medRxiv** | 鉁?| 鉁?| 鍖诲棰勫嵃鏈?|
| **Google Scholar** | 鉁?| 鉂?| 缁煎悎瀛︽湳鎼滅储 |
| **Semantic Scholar** | 鉁?| 鉁?| AI 椹卞姩鐨勫鏈悳绱?|
| **CrossRef** | 鉁?| 鉂?| DOI 鍏冩暟鎹簱 |
| **IACR** | 鉁?| 鉁?| 瀵嗙爜瀛﹁鏂?|

## 蹇€熶娇鐢?

### 鎼滅储璁烘枃

```bash
# 鎼滅储 arXiv
python scripts/search.py arxiv "large language model" --max 10

# 鎼滅储 PubMed锛堝尰瀛︼級
python scripts/search.py pubmed "cancer immunotherapy" --max 10

# 鎼滅储 bioRxiv锛堢敓鐗╁棰勫嵃鏈級
python scripts/search.py biorxiv "CRISPR gene editing" --max 10

# 鎼滅储 Semantic Scholar
python scripts/search.py semantic "transformer architecture" --max 10

# 鎼滅储 CrossRef锛堥€氳繃 DOI 鏁版嵁搴擄級
python scripts/search.py crossref "climate change" --max 10
```

### 涓嬭浇璁烘枃 PDF

```bash
# 涓嬭浇 arXiv 璁烘枃
python scripts/download.py arxiv 2301.07041 --output ./papers

# 涓嬭浇 bioRxiv 璁烘枃
python scripts/download.py biorxiv 10.1101/2023.01.01.123456 --output ./papers

# 涓嬭浇 IACR 璁烘枃
python scripts/download.py iacr 2023/123 --output ./papers
```

### 閫氳繃 DOI 鑾峰彇璁烘枃淇℃伅

```bash
python scripts/search.py doi 10.1038/nature12373
```

## 杈撳嚭鏍煎紡

鎼滅储缁撴灉浠?JSON 鏍煎紡杈撳嚭锛屽寘鍚細

```json
{
  "paper_id": "2301.07041",
  "title": "Paper Title",
  "authors": ["Author 1", "Author 2"],
  "abstract": "Abstract text...",
  "url": "https://arxiv.org/abs/2301.07041",
  "pdf_url": "https://arxiv.org/pdf/2301.07041.pdf",
  "published_date": "2023-01-17",
  "source": "arxiv",
  "categories": ["cs.CL", "cs.AI"],
  "doi": "10.48550/arXiv.2301.07041"
}
```

## 涓?deep-research 閰嶅悎浣跨敤

鍦?`deep-research` 鐨?Step 2锛堣祫鏂欏垎灞傦級涓紝浣跨敤鏈?skill 鑾峰彇 L1 绾у埆瀛︽湳璧勬枡锛?

```markdown
## 璧勬枡鍒嗗眰寤鸿

| 灞傜骇 | 璧勬枡绫诲瀷 | 鑾峰彇鏂瑰紡 |
|------|----------|----------|
| **L1** | arXiv 棰勫嵃鏈€丳ubMed 璁烘枃 | 浣跨敤 paper-search skill |
| **L2** | 瀹樻柟鍗氬銆佹妧鏈紨璁?| WebSearch |
| **L3** | 鏉冨▉濯掍綋銆佷笓瀹惰В璇?| WebSearch |
| **L4** | 绀惧尯璁ㄨ銆佷釜浜哄崥瀹?| WebSearch |
```

## 涓?deep-research 娣卞害闆嗘垚

### 浣滀负绗竷杞悳绱㈢瓥鐣?

鍦?`deep-research` 鐨?7 杞悳绱㈢瓥鐣ヤ腑锛屾湰 skill 璐熻矗绗竷杞€屽鏈墠娌挎悳绱€嶏細

```markdown
## 绗竷杞悳绱㈡墽琛屾祦绋?

1. **鍒ゆ柇鏄惁闇€瑕佸鏈悳绱?*锛?
   - 涓婚娑夊強绉戝鍘熺悊銆佺畻娉曘€佹妧鏈満鍒?鈫?蹇呴』鎵ц
   - 闇€瑕佸紩鐢ㄥ鏈鏂囨敮鎾戠粨璁?鈫?蹇呴』鎵ц
   - 鐢ㄦ埛鏄庣‘瑕佹眰瀛︽湳鏂囩尞鏀寔 鈫?蹇呴』鎵ц

2. **閫夋嫨鍚堥€傜殑鏁版嵁搴?*锛?
   | 棰嗗煙 | 鎺ㄨ崘鏁版嵁搴?| 鍛戒护 |
   |------|-----------|------|
   | AI/鏈哄櫒瀛︿範/娣卞害瀛︿範 | arXiv | `python scripts/search.py arxiv "<鍏抽敭璇?" --max 10` |
   | 璁＄畻鏈虹瀛?绠楁硶 | arXiv + Semantic Scholar | 涓よ€呴兘鎼滅储 |
   | 鐢熺墿鍖诲/涓村簥 | PubMed + bioRxiv | 涓よ€呴兘鎼滅储 |
   | 璺ㄩ鍩熺患鍚?| Semantic Scholar | `python scripts/search.py semantic "<鍏抽敭璇?" --max 10` |
   | 瀵嗙爜瀛?瀹夊叏 | IACR | `python scripts/search.py iacr "<鍏抽敭璇?" --max 10` |

3. **璧勬枡褰掔被**锛?
   - 鎵€鏈夊鏈鏂囪嚜鍔ㄥ綊绫讳负 **L1 绾у埆**
   - 鍦?`01_璧勬枡鏉ユ簮.md` 涓爣娉ㄦ潵婧愭暟鎹簱鍜岃鏂?ID
```

### 瀛︽湳璧勬枡璁板綍妯℃澘

鍦?deep-research 鐨?`01_璧勬枡鏉ユ簮.md` 涓紝瀛︽湳璁烘枃搴斾娇鐢ㄤ互涓嬫牸寮忥細

```markdown
## 璧勬枡 #[搴忓彿] (瀛︽湳璁烘枃)
- **鏍囬**锛歔璁烘枃鏍囬]
- **浣滆€?*锛歔浣滆€呭垪琛╙
- **鏉ユ簮**锛歛rXiv / PubMed / bioRxiv / Semantic Scholar
- **ID**锛歛rXiv:2301.07041 / PMID:12345678 / DOI:10.xxxx
- **閾炬帴**锛歔URL]
- **灞傜骇**锛歀1锛堝鏈鏂囷級
- **鍙戝竷鏃ユ湡**锛歔YYYY-MM-DD]
- **鎽樿**锛歔璁烘枃鎽樿]
- **涓庡瓙闂鍏宠仈**锛歔瀵瑰簲鍝釜瀛愰棶棰榏
```

### 鎼滅储鍏抽敭璇嶇瓥鐣?

涓鸿幏寰楁渶浣虫悳绱㈢粨鏋滐紝寤鸿锛?

1. **浣跨敤鑻辨枃鍏抽敭璇?*锛氬鏈暟鎹簱浠ヨ嫳鏂囦负涓?
2. **缁勫悎澶氫釜鍏抽敭璇?*锛歚"transformer attention mechanism"`
3. **浣跨敤棰嗗煙鏈**锛氶伩鍏嶈繃浜庨€氫織鐨勮〃杩?
4. **闄愬埗鏃堕棿鑼冨洿**锛氬浜庡揩閫熷彂灞曠殑棰嗗煙锛屼紭鍏堟悳绱㈣繎 2 骞寸殑璁烘枃

## 渚濊禆瀹夎

```bash
pip install requests feedparser PyPDF2 scholarly httpx beautifulsoup4
```

## 甯歌闂

### Google Scholar 琚檺鍒?
Google Scholar 鏈夊弽鐖満鍒讹紝棰戠箒璇锋眰鍙兘琚檺鍒躲€傚缓璁細
- 闄嶄綆璇锋眰棰戠巼
- 浣跨敤浠ｇ悊
- 浼樺厛浣跨敤 Semantic Scholar 鏇夸唬

### PubMed 鏃犳硶涓嬭浇 PDF
PubMed 鏄储寮曟暟鎹簱锛屼笉鐩存帴鎻愪緵 PDF銆傚彲浠ワ細
- 浣跨敤璁烘枃鐨?DOI 鍒板嚭鐗堝晢缃戠珯涓嬭浇
- 妫€鏌?PubMed Central (PMC) 鏄惁鏈夊厤璐瑰叏鏂?

### Semantic Scholar API Key
鍙€夐厤缃?API Key 鑾峰緱鏇撮珮閰嶉锛?
```bash
export SEMANTIC_SCHOLAR_API_KEY="your_key"
```

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 与 deep-research 配合时作为第七轮搜索策略
- 搜索结果自动归类为 L1 级别学术资料
- Scrapling 作为 HTTP 层时应用 _http_get 封装统一处理，保持各 download_* 函数签名不变

### Known Fixes & Workarounds
- scrapling 0.4 中 PlayWrightFetcher 已改名为 DynamicFetcher
- scrapling 0.4 Response 对象属性 .html → .html_content，.content → .body
- scrapling 需要 pip install scrapling[all] 才能获得完整依赖（browserforge、patchright）
- download.py 的 _http_get fallback 中 resp.content 应改为 resp.body（scrapling Response）
- search.py 和 download.py 均需在 import sys 后添加 sys.stdout/stderr.reconfigure(encoding=utf-8) 修复 Windows GBK 编码问题，两个脚本都要改

### Custom Instruction Injection

学术搜索建议使用英文关键词以获得更好结果