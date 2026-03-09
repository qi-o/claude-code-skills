---
name: http-retry
version: 1.0.0
description: |
  HTTP 璇锋眰閲嶈瘯宸ュ叿锛屾敮鎸佹寚鏁伴€€閬裤€佺啍鏂櫒鍜?429 闄愭祦澶勭悊銆?
  瑙﹀彂璇嶏細http retry銆侀噸璇曘€乤pi error銆?29銆乺ate limit銆乪xponential backoff
github_url: ""
local_only: true
license: MIT
allowed-tools: "Bash(python:*) Read"
metadata:
  category: utilities
---

# HTTP Retry

HTTP 璇锋眰閲嶈瘯宸ュ叿锛屾彁渚涗紒涓氱骇鍙潬鎬т繚闅溿€?

## 鏍稿績鍔熻兘

- **鎸囨暟閫€閬?(Exponential Backoff)**: 閲嶈瘯闂撮殧鏃堕棿鎸囨暟澧為暱锛岄伩鍏嶉绻佽姹?
- **鐔旀柇鍣?(Circuit Breaker)**: 杩炵画澶辫触鍚庤嚜鍔ㄧ啍鏂紝闃叉绾ц仈鏁呴殰
- **429 澶勭悊**: 鑷姩瑙ｆ瀽 Retry-After 鍝嶅簲澶?
- **瑁呴グ鍣?绫诲弻 API**: 鐏垫椿闆嗘垚鏂瑰紡

## 鑴氭湰鐩綍

鑴氭湰浣嶄簬 `scripts/` 瀛愮洰褰曘€?

| 鑴氭湰 | 鐢ㄩ€?|
|------|------|
| `scripts/retry.py` | 閲嶈瘯閫昏緫鏍稿績瀹炵幇 |

## 浣跨敤鏂瑰紡

### 瑁呴グ鍣ㄦ柟寮?

```python
from retry import retry

@retry(max_attempts=3, initial_delay=1, max_delay=30, backoff_factor=2)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

### 绫绘柟寮?

```python
from retry import RetryHandler

handler = RetryHandler(
    max_attempts=3,
    initial_delay=1,
    max_delay=30,
    backoff_factor=2,
    circuit_breaker_threshold=5,
    circuit_breaker_timeout=60
)

result = handler.execute(lambda: requests.get(url))
```

## 鍙傛暟璇存槑

| 鍙傛暟 | 绫诲瀷 | 璇存槑 | 榛樿鍊?|
|------|------|------|--------|
| `max_attempts` | int | 鏈€澶ч噸璇曟鏁?| 3 |
| `initial_delay` | float | 鍒濆寤惰繜锛堢锛?| 1 |
| `max_delay` | float | 鏈€澶у欢杩燂紙绉掞級 | 60 |
| `backoff_factor` | float | 閫€閬垮洜瀛?| 2.0 |
| `retry_on_status` | list | 闇€瑕侀噸璇曠殑 HTTP 鐘舵€佺爜 | [429, 500, 502, 503, 504] |
| `circuit_breaker_threshold` | int | 鐔旀柇鍣ㄥけ璐ラ槇鍊?| 5 |
| `circuit_breaker_timeout` | float | 鐔旀柇鍣ㄦ仮澶嶈秴鏃讹紙绉掞級 | 60 |

## 429 澶勭悊

鑷姩澶勭悊閫熺巼闄愬埗鍝嶅簲锛?

1. 妫€娴?429 鐘舵€佺爜
2. 瑙ｆ瀽 `Retry-After` 鍝嶅簲澶?
3. 浣跨敤鏈嶅姟鍣ㄦ寚瀹氱殑鏃堕棿绛夊緟
4. 濡傛灉娌℃湁 `Retry-After`锛屼娇鐢ㄦ寚鏁伴€€閬?

```python
# 绀轰緥锛氬鐞?GitHub API 闄愭祦
@retry(max_attempts=5, initial_delay=2)
def github_api_request(endpoint):
    response = requests.get(f"https://api.github.com/{endpoint}")
    if response.status_code == 429:
        # 鑷姩绛夊緟 Retry-After 绉?
        retry_after = int(response.headers.get("Retry-After", 60))
        time.sleep(retry_after)
    response.raise_for_status()
    return response.json()
```

## 鐔旀柇鍣ㄦā寮?

杩炵画澶辫触杈惧埌闃堝€煎悗锛岀啍鏂櫒鎵撳紑锛屽悗缁姹傜洿鎺ュけ璐ヨ€屼笉鍙戦€侊細

```
姝ｅ父 鈫?澶辫触绱Н 鈫?鐔旀柇鎵撳紑 鈫?瓒呮椂 鈫?鍗婂紑 鈫?姝ｅ父
```

```python
@retry(circuit_breaker_threshold=3, circuit_breaker_timeout=30)
def unreliable_api_call():
    # 杩炵画3娆″け璐ュ悗锛?0绉掑唴鎵€鏈夎皟鐢ㄧ洿鎺ュけ璐?
    pass
```

## 渚濊禆

- Python 3.8+
- requests (鍙€夛紝鐢ㄤ簬 HTTP 璇锋眰)

## 瀹夎

```bash
pip install requests
```

## 瀹屾暣绀轰緥

```python
import requests
from retry import retry, RetryHandler

# 浣跨敤瑁呴グ鍣?
@retry(max_attempts=5, initial_delay=1, backoff_factor=2, max_delay=60)
def call_api(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# 浣跨敤绫?
handler = RetryHandler(
    max_attempts=3,
    initial_delay=1,
    circuit_breaker_threshold=5,
    circuit_breaker_timeout=60
)

result = handler.execute(lambda: requests.get("https://api.example.com/data"))
```

---

## 鐗堟湰鍘嗗彶

- **v1.0.0** (2026-02-20): 鍒濆鐗堟湰
  - 鎸囨暟閫€閬块噸璇?
  - 鐔旀柇鍣ㄦā寮?
  - 429 鐘舵€佺爜澶勭悊
  - Retry-After 澶磋В鏋?
