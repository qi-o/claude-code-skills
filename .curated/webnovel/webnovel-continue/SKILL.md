---
name: webnovel-continue
description: 绠€鍖栫増缁啓鍛戒护銆備粠鎸囧畾绔犺妭鎴栨渶鏂扮珷鑺?1寮€濮嬪啓浣滐紝绫讳技 /webnovel-write 鐨勫揩鎹锋柟寮忋€?
allowed-tools: Read Write Edit Grep Bash Task
---

# Continue Writing (绠€鍖栫画鍐欐ā鍧?

## 鐩爣

- 鎻愪緵涓€涓畝鍖栫増鐨勭画鍐欏懡浠?
- 鏀寔浠庢寚瀹氱珷鑺傚彿寮€濮嬪啓浣?
- 鑷姩妫€娴嬭捣濮嬬珷鑺傦紙鏈€鏂扮珷+1锛?

## 浣跨敤鏂瑰紡

```
/webnovel-continue           # 浠庢渶鏂扮珷鑺?1寮€濮嬪啓
/webnovel-continue 50        # 浠庣50绔犲紑濮嬪啓
/webnovel-continue latest    # 鍚屼笂锛屼粠鏈€鏂扮珷鑺?1寮€濮嬪啓
/webnovel-continue next      # 鍚屼笂锛屼粠鏈€鏂扮珷鑺?1寮€濮嬪啓
```

## 鎵ц娴佺▼

### 1. 纭畾璧峰绔犺妭

鏍规嵁鍙傛暟纭畾瑕佸啓鐨勭珷鑺傚彿锛?

| 鍙傛暟 | 琛屼负 |
|------|------|
| 鏃犲弬鏁?| 鑷姩鏌ユ壘鏈€鏂扮珷鑺傦紝+1 |
| 鏁板瓧 N | 浠庣 N 绔犲紑濮嬪啓 |
| `latest` / `next` | 浠庢渶鏂扮珷鑺?1寮€濮嬪啓 |

### 2. 妫€娴嬮」鐩?

纭褰撳墠宸ヤ綔鐩綍涓嬫湁鍙敤鐨勭綉鏂囬」鐩細

```bash
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"
export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

### 3. 妫€娴嬭捣濮嬬珷鑺?

鏌ヨ宸叉湁绔犺妭锛?

```bash
# 鍒楀嚭鎵€鏈夋鏂囩珷鑺?
ls "${PROJECT_ROOT}/姝ｆ枃/" | sort -V

# 鎴栦粠 state.json 璇诲彇褰撳墠杩涘害
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" state get-progress
```

### 4. 鎵х瑪鍐欎綔

纭畾绔犺妭鍙峰悗锛岃皟鐢?`/webnovel-write`锛?

```bash
# 渚嬪纭畾瑕佸啓绗?15 绔?
/webnovel-write 15
```

## 瀹炵幇閫昏緫

### 鑷姩妫€娴嬫渶鏂扮珷鑺?

1. 鎵弿 `姝ｆ枃/` 鐩綍
2. 鎻愬彇绔犺妭缂栧彿锛堟鍒欏尮閰?`绗?\d+)绔燻锛?
3. 鍙栨渶澶х紪鍙?+ 1

```python
import re
from pathlib import Path

def get_next_chapter(project_root: str) -> int:
    """妫€娴嬩笅涓€涓珷鑺傚彿"""
    content_dir = Path(project_root) / "姝ｆ枃"
    if not content_dir.exists():
        return 1

    max_num = 0
    pattern = re.compile(r"绗?\d+)绔?)

    for f in content_dir.glob("*.md"):
        match = pattern.search(f.stem)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    return max_num + 1
```

### 鍙傛暟瑙ｆ瀽

| 杈撳叆 | 瑙ｆ瀽缁撴灉 |
|------|----------|
| `/webnovel-continue` | next_chapter = auto_detect() |
| `/webnovel-continue 5` | next_chapter = 5 |
| `/webnovel-continue 10` | next_chapter = 10 |
| `/webnovel-continue latest` | next_chapter = auto_detect() |
| `/webnovel-continue next` | next_chapter = auto_detect() |

## 閿欒澶勭悊

| 閿欒 | 澶勭悊 |
|------|------|
| 鏃犻」鐩?| 鎻愮ず鍏堢敤 `/webnovel-import` 鎴?`/webnovel-init` |
| 鐩綍涓嶅瓨鍦?| 鍒涘缓 `姝ｆ枃/` 鐩綍 |
| 绔犺妭鏂囦欢宸插瓨鍦?| 璇㈤棶鏄惁瑕嗙洊鎴栬烦杩?|

## 绀轰緥瀵硅瘽

### 绀轰緥1锛氳嚜鍔ㄦ娴?

```
鐢ㄦ埛: /webnovel-continue
绯荤粺: 妫€娴嬪埌鏈€鏂扮珷鑺備负绗?2绔狅紝灏嗕粠绗?3绔犲紑濮嬪啓浣溿€?
鈫?璋冪敤 /webnovel-write 13
```

### 绀轰緥2锛氭寚瀹氱珷鑺?

```
鐢ㄦ埛: /webnovel-continue 50
绯荤粺: 纭浠庣50绔犲紑濮嬪啓浣溿€?
鈫?璋冪敤 /webnovel-write 50
```

### 绀轰緥3锛氭棤椤圭洰

```
鐢ㄦ埛: /webnovel-continue
閿欒: 鏈娴嬪埌缃戞枃椤圭洰銆?
鎻愮ず: 璇峰厛浣跨敤 /webnovel-import 瀵煎叆宸叉湁灏忚锛屾垨浣跨敤 /webnovel-init 鍒涘缓鏂伴」鐩€?
```

## 涓?webnovel-write 鐨勫叧绯?

`/webnovel-continue` 鏄?`/webnovel-write` 鐨勭畝鍖栧叆鍙ｏ細

- **鐩稿悓鐐?*锛氭渶缁堥兘璋冪敤鐩稿悓鐨勫啓浣滄祦绋?
- **涓嶅悓鐐?*锛?
  - `webnovel-write` 闇€瑕佹槑纭寚瀹氱珷鑺傚彿
  - `webnovel-continue` 鏀寔鑷姩妫€娴嬭捣濮嬬珷鑺?

## 楠岃瘉

鎴愬姛鏍囧噯锛?
- 姝ｇ‘瑙ｆ瀽鐢ㄦ埛杈撳叆鐨勭珷鑺傚彿
- 姝ｇ‘妫€娴嬫渶鏂扮珷鑺傦紙褰撳弬鏁颁负绌烘椂锛?
- 鎴愬姛璋冪敤 `/webnovel-write` 寮€濮嬪啓浣?
