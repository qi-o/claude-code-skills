# Alphapolis (alphapolis.co.jp)

## 2025骞?鏈堟洿鏂帮細AWS WAF淇濇姢

**閲嶈鍙樻洿**锛欰lphapolis鐜板凡鍚敤AWS WAF淇濇姢锛岀洿鎺ヤ娇鐢╮equests浼氳繑鍥?02鐘舵€佺爜銆?
### 瑙ｅ喅鏂规锛氫娇鐢≒laywright

```bash
pip install scrapling[all] beautifulsoup4
scrapling install
```

浣跨敤 `scripts/alphapolis.py` 鑴氭湰锛岃鑴氭湰浣跨敤Playwright娴忚鍣ㄨ嚜鍔ㄥ寲缁曡繃WAF銆?
## 缃戠珯鐗圭偣
- 绫诲瀷锛欰JAX鍔ㄦ€佸姞杞?+ AWS WAF淇濇姢
- 鍙嶇埇鏈哄埗锛歐AF + CSRF Token + Session妫€娴?- 姝ｆ枃閫夋嫨鍣細`#novelBody`

## 鏃х増鏂规锛堟棤WAF鏃跺彲鐢級

濡傛灉WAF鏈Е鍙戯紝鍙娇鐢╮equests鏂规锛?- 鍏抽敭锛氭瘡绔犱娇鐢ㄧ嫭绔媠ession
- API锛歚POST /novel/episode_body`
- 闇€瑕侊細X-XSRF-TOKEN澶?
## 甯歌閿欒

| 閿欒 | 鍘熷洜 | 瑙ｅ喅 |
|------|------|------|
| 202鐘舵€佺爜 | AWS WAF | 浣跨敤Playwright |
| 419 | XSRF-TOKEN缂哄け | 娣诲姞X-XSRF-TOKEN澶?|
| 鍓峃绔犵┖ | 鍏辩敤session | 姣忕珷鏂板缓session |
| token鎵句笉鍒?| 鍏堣闂簡鐩綍椤?| 鐩存帴璁块棶绔犺妭椤?|
