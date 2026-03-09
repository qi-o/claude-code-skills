---
name: agent-self-heal
version: 1.0.0
description: |
  Agent 鑷垜璇婃柇涓庝慨澶嶅伐鍏枫€傚疄鐜板叏灞€閿欒鎹曡幏鏈哄埗锛岄€氳繃妯″紡鍖归厤杩涜鏍瑰洜鍒嗘瀽锛?
  鑷姩淇甯歌闂锛堝垱寤虹己澶辨枃浠躲€佷慨澶嶆潈闄愩€佸畨瑁呬緷璧栵級锛岀敓鎴愯嚜璇婃柇鎶ュ憡銆?
  瑙﹀彂璇嶏細self-heal銆佽嚜妫€銆乨ebug銆佽瘖鏂€乪rror analysis銆乺oot cause
github_url: https://github.com/anthropics/claude-code
github_hash: 53a5f3ee0703c2ab1b6d1dd18d8ab65187f9b8ad
source: skills/agent-self-heal
license: MIT
allowed-tools: "Bash Read Write Glob Grep Edit Task"
metadata:
  category: developer-tools
---

# Agent Self-Heal

Agent 鑷垜璇婃柇涓庝慨澶嶅伐鍏凤紝甯姪 Agent 鑷富璇嗗埆鍜屼慨澶嶅父瑙侀敊璇€?

## 鏍稿績鍔熻兘

- **鍏ㄥ眬閿欒鎹曡幏**: 鐩戝惉骞舵崟鑾峰悇绫昏繍琛屾椂閿欒
- **鏍瑰洜鍒嗘瀽**: 閫氳繃閿欒妯″紡鍖归厤瀹氫綅闂鏍规簮
- **鑷姩淇**: 鑷姩澶勭悊甯歌闂锛堟枃浠剁己澶便€佹潈闄愰敊璇€佷緷璧栭棶棰橈級
- **璇婃柇鎶ュ憡**: 鐢熸垚缁撴瀯鍖栫殑鑷瘖鏂姤鍛?

## 鑴氭湰鐩綍

鑴氭湰浣嶄簬 `scripts/` 瀛愮洰褰曘€傚皢 `${SKILL_DIR}` 鏇挎崲涓?SKILL.md 鎵€鍦ㄧ洰褰曡矾寰勩€?

| 鑴氭湰 | 鐢ㄩ€?|
|------|------|
| `scripts/self-heal.ts` | 涓昏瘖鏂笌淇鑴氭湰 |

## 閿欒绫诲埆涓庝慨澶嶇瓥鐣?

### 1. 鏂囦欢鏈壘鍒?(File Not Found)

- **閿欒妯″紡**: `ENOENT: no such file or directory`, `File does not exist`
- **淇绛栫暐**:
  - 妫€鏌ユ枃浠惰矾寰勬槸鍚︽纭?
  - 鎻愮ず鐢ㄦ埛鍒涘缓缂哄け鏂囦欢
  - 鎻愪緵鏂囦欢妯℃澘寤鸿

### 2. 鏉冮檺鎷掔粷 (Permission Denied)

- **閿欒妯″紡**: `EACCES: permission denied`, `EPERM: operation not permitted`
- **淇绛栫暐**:
  - 妫€鏌ユ枃浠?鐩綍鏉冮檺
  - 鎻愪緵淇鏉冮檺鍛戒护锛坈hmod / icacls锛?

### 3. 妯″潡鏈壘鍒?(Module Not Found)

- **閿欒妯″紡**: `Cannot find module`, `Module not found`, `ERR_MODULE_NOT_FOUND`
- **淇绛栫暐**:
  - 妫€鏌?package.json 渚濊禆
  - 鎻愪緵 npm install / bun install 鍛戒护
  - 寤鸿姝ｇ‘鐨勫鍏ヨ矾寰?

### 4. 璇硶閿欒 (Syntax Error)

- **閿欒妯″紡**: `SyntaxError`, `unexpected token`, `unexpected string`
- **淇绛栫暐**:
  - 瀹氫綅閿欒琛屽彿
  - 鎻愪緵甯歌璇硶閿欒淇寤鸿
  - 鎸囧嚭鍙兘鐨勬嫭鍙?寮曞彿涓嶅尮閰?

### 5. 绫诲瀷閿欒 (Type Error)

- **閿欒妯″紡**: `TypeError`, `Cannot read property`, `undefined is not a function`
- **淇绛栫暐**:
  - 鍒嗘瀽绫诲瀷涓嶅尮閰嶅師鍥?
  - 鎻愪緵绌哄€兼鏌ュ缓璁?
  - 鎸囧嚭鍙兘鐨?API 浣跨敤閿欒

### 6. 缃戠粶閿欒 (Network Error)

- **閿欒妯″紡**: `ECONNREFUSED`, `ETIMEDOUT`, `ENOTFOUND`, `fetch failed`
- **淇绛栫暐**:
  - 妫€鏌ョ綉缁滆繛鎺?
  - 鎻愪緵閲嶈瘯寤鸿锛堝甫 http-retry锛?
  - 妫€鏌?URL 鏄惁姝ｇ‘

## 浣跨敤鏂规硶

### 鏂瑰紡涓€锛氬懡浠よ璋冪敤

```bash
npx -y bun ${SKILL_DIR}/scripts/self-heal.ts <error-message> [options]
```

### 鏂瑰紡浜岋細浣滀负 Skill 璋冪敤

褰撻亣鍒伴敊璇椂锛岀洿鎺ヤ娇鐢ㄤ互涓嬭Е鍙戣瘝锛?
- `self-heal`
- `鑷`
- `debug`
- `璇婃柇`
- `error analysis`
- `root cause`

## 鍙傛暟璇存槑

| 鍙傛暟 |  | 璇存槑 | 榛樿鍊?|
|------|--------|------|--------鐭弬鏁皘
| `<error-message>` | - | 閿欒淇℃伅锛堝瓧绗︿覆鎴?JSON锛?| 蹇呴渶 |
| `--context` | `-c` | 闄勫姞涓婁笅鏂囦俊鎭?| "" |
| `--auto-fix` | `-a` | 鏄惁灏濊瘯鑷姩淇 | false |
| `--report` | `-r` | 鐢熸垚璇婃柇鎶ュ憡 | false |
| `--json` | - | JSON 鏍煎紡杈撳嚭 | false |

## 浣跨敤绀轰緥

### 鍩烘湰璇婃柇

```bash
/self-heal "Error: Cannot find module './utils'"
```

杈撳嚭锛?
```
馃攳 閿欒鍒嗘瀽

閿欒绫诲瀷: Module Not Found
鍙兘鍘熷洜:
  1. 妯″潡璺緞涓嶆纭?
  2. 妯″潡鏈畨瑁?
  3. 鏂囦欢鎵╁睍鍚嶇己澶?

寤鸿鎿嶄綔:
  - 妫€鏌ユ枃浠惰矾寰勬槸鍚︽纭?
  - 纭鏂囦欢鎵╁睍鍚?(.ts, .js, .json)
  - 杩愯 npm install 瀹夎渚濊禆
```

### 鑷姩淇妯″紡

```bash
/self-heal "Error: ENOENT: no such file or directory" --auto-fix
```

### 鐢熸垚璇婃柇鎶ュ憡

```bash
/self-heal --report --json
```

## 閿欒瑙勫垯鍙傝€?

璇︾粏閿欒妯″紡涓庝慨澶嶈鍒欒鍙傞槄 `references/error-rules.md`銆?

---

## 鐗堟湰鍘嗗彶

- **v1.0.0** (2026-02-20): 鍒濆鐗堟湰
  - 瀹炵幇鍏ㄥ眬閿欒鎹曡幏鏈哄埗
  - 鏀寔 6 澶х被閿欒妯″紡璇嗗埆
  - 鎻愪緵鑷姩淇寤鸿
  - 鐢熸垚鑷瘖鏂姤鍛?
