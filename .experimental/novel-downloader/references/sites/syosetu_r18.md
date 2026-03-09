# Syosetu R18 (novel18.syosetu.com)

## 缃戠珯鐗圭偣
- 绫诲瀷锛氶潤鎬佸唴瀹?- 骞撮緞楠岃瘉锛氶渶瑕佽缃?`over18=yes` cookie
- 涓庢櫘閫歴yosetu.com閫夋嫨鍣ㄤ笉鍚?
## 鍏抽敭閰嶇疆

```python
# 璁剧疆骞撮緞楠岃瘉cookie
session.cookies.set('over18', 'yes', domain='.syosetu.com')
```

## 閫夋嫨鍣?
| 鍏冪礌 | 閫夋嫨鍣?|
|------|--------|
| 灏忚鏍囬 | `.novel_title, .p-novel__title` |
| 浣滆€?| `.novel_writername a, .p-novel__author a` |
| 绔犺妭鍒楄〃 | `.index_box a, .p-eplist__sublist a` |
| 姝ｆ枃 | `.p-novel__body` (R18绔? 鎴?`#novel_honbun` (鏅€氱珯) |
| 鍓嶈█ | `#novel_p` |
| 鍚庤 | `#novel_a` |

## 娉ㄦ剰浜嬮」

1. **R18绔欎娇鐢ㄤ笉鍚岄€夋嫨鍣?*锛歚.p-novel__body` 鑰岄潪 `#novel_honbun`
2. **闇€瑕佸勾榫勯獙璇乧ookie**锛氬惁鍒欎細閲嶅畾鍚戝埌楠岃瘉椤甸潰
3. 寤鸿寤惰繜1绉?绔?
## 鑴氭湰

浣跨敤 `scripts/syosetu_r18.py`
