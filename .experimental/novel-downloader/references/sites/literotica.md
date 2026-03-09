# Literotica (literotica.com)

## 缃戠珯鐗圭偣
- 绫诲瀷锛歋PA搴旂敤锛屾湇鍔＄娓叉煋
- 鍙嶇埇鏈哄埗锛欻TTP/2鍗忚闂瀵艰嚧requests/playwright澶辫触
- 姝ｆ枃閫夋嫨鍣細`div[class*="_article__content"]`
- 鍒嗛〉锛氱珷鑺傚唴鍒嗛〉锛孶RL鏍煎紡 `?page=N`

## 瑙ｅ喅鏂规锛氫娇鐢╟url

鐢变簬HTTP/2鍗忚闂锛岄渶瑕佷娇鐢╟url鑾峰彇椤甸潰锛?
```python
import subprocess

def fetch_url(url):
    result = subprocess.run([
        'curl', '-s', '-L',
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '-H', 'Accept: text/html,application/xhtml+xml',
        url
    ], capture_output=True, text=True, timeout=60)
    return result.stdout
```

## URL鏍煎紡
- 绯诲垪椤碉細`https://www.literotica.com/series/se/{slug}`
- 绔犺妭椤碉細`https://www.literotica.com/s/{slug}-ch-{num}`
- 鍒嗛〉锛歚https://www.literotica.com/s/{slug}-ch-{num}?page={page}`

## 閫夋嫨鍣?
| 鍏冪礌 | 閫夋嫨鍣?|
|------|--------|
| 姝ｆ枃 | `div[class*="_article__content"]` |
| 浣滆€?| `a[href*="/authors/"]` |
| 涓嬩竴椤?| `a[href*="?page=N"]` |

## 娉ㄦ剰浜嬮」

1. **HTTP/2闂**锛歳equests鍜宲laywright閮戒細閬囧埌鍗忚閿欒锛屽繀椤讳娇鐢╟url
2. **绔犺妭鍐呭垎椤?*锛氭瘡绔犲彲鑳芥湁澶氶〉锛岄渶瑕佸惊鐜幏鍙?3. **鍒嗛〉妫€娴?*锛氶€氳繃鏌ユ壘涓嬩竴椤甸摼鎺ュ垽鏂槸鍚︽湁鏇村椤?4. 寤鸿寤惰繜1绉?绔狅紝0.5绉?椤?
## 鑴氭湰

浣跨敤 `scripts/literotica.py`锛岄渶瑕佷慨鏀?`SERIES_URL` 鍜?`OUTPUT_FILE` 鍙橀噺
