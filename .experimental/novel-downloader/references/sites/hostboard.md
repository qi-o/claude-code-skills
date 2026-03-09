# Hostboard.com (vBulletin 璁哄潧)

## 缃戠珯鐗圭偣
- 绫诲瀷锛歷Bulletin 璁哄潧锛屽皬璇翠互甯栧瓙褰㈠紡鍙戝竷
- 鍙嶇埇鏈哄埗锛欳loudflare Turnstile 楠岃瘉锛?03 + JS Challenge锛?- 姝ｆ枃閫夋嫨鍣細`[id^=post_message_]`
- 鍐呭缁撴瀯锛氬皬璇存鏂囧湪闀垮笘瀛愪腑锛岃瘎璁轰负鐭笘瀛?- 鍒嗛〉锛歷Bulletin 鏍囧噯鍒嗛〉 `?page=N`

## 瑙ｅ喅鏂规锛欴rissionPage

Cloudflare Turnstile 鏃犳硶琚?requests銆乧url銆乧loudscraper銆乧url_cffi銆丳laywright 缁曡繃銆?蹇呴』浣跨敤 DrissionPage锛堝熀浜?CDP 鍗忚鎺у埗鐪熷疄娴忚鍣級锛?
```python
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co.set_argument('--no-sandbox')
page = ChromiumPage(co)
page.get(url)
# 绛夊緟 Cloudflare 楠岃瘉閫氳繃锛堢害 10-20 绉掞級
# 妫€娴嬫柟寮忥細椤甸潰闀垮害 > 30000 涓旀爣棰樹笉鍚?"璇风◢鍊? / "Just a moment"
```

## URL鏍煎紡
- 甯栧瓙椤碉細`https://www.hostboard.com/forums/f{forum_id}/{thread_id}-{slug}.html`
- 鍒嗛〉锛歚...html?page=2`

## 閫夋嫨鍣?
| 鍏冪礌 | 閫夋嫨鍣?|
|------|--------|
| 姝ｆ枃 | `[id^=post_message_]` |
| 鏍囬 | `<title>` (鍘绘帀 "Thread:" 鍓嶇紑) |
| 鍒嗛〉 | `.pagenav a[href*="page="]` |

## 鍐呭杩囨护绛栫暐

璁哄潧甯栧瓙娣峰悎浜嗗皬璇存鏂囧拰璇昏€呰瘎璁恒€傞€氳繃鍐呭闀垮害鍖哄垎锛?- **>1000 瀛楃** 鈫?灏忚姝ｆ枃
- **<1000 瀛楃** 鈫?璇勮/鍥炲锛堣繃婊ゆ帀锛?
姝ら槇鍊煎湪瀹炴祴涓晥鏋滆壇濂斤細姝ｆ枃閫氬父鏁颁竾瀛楃锛岃瘎璁洪€氬父鍑犵櫨瀛楃銆?
## 娉ㄦ剰浜嬮」

1. **Cloudflare Turnstile**锛氫互涓嬫柟娉曞潎鏃犳硶缁曡繃锛屽彧鏈?DrissionPage 鏈夋晥锛?   - requests / curl / cloudscraper / curl_cffi 鈫?403
   - Playwright (鍚?stealth) 鈫?鍗″湪 "Just a moment..." 涓嶉€氳繃
   - undetected-chromedriver 鈫?ChromeDriver 鐗堟湰鍏煎闂
2. **绛夊緟鏃堕棿**锛欳loudflare 楠岃瘉閫氬父闇€瑕?10-20 绉?3. **澶嶇敤娴忚鍣ㄥ疄渚?*锛氭壒閲忎笅杞芥椂淇濇寔鍚屼竴涓?ChromiumPage 瀹炰緥锛岀涓€涓?URL 閫氳繃楠岃瘉鍚庡悗缁?URL 鏃犻渶鍐嶇瓑
4. **鏂囦欢鍛藉悕**锛氫娇鐢ㄥ笘瀛愭爣棰樺懡鍚嶏紝闇€娓呯悊闈炴硶鏂囦欢鍚嶅瓧绗?
## 渚濊禆

```bash
pip install DrissionPage beautifulsoup4
```

## 鑴氭湰

浣跨敤 `scripts/hostboard.py`锛岄渶瑕佷慨鏀?`URLS` 鍒楄〃鍜?`OUTPUT_DIR` 鍙橀噺
