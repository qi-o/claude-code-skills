---
name: gitnexus
description: |
  GitNexus 浠ｇ爜鐭ヨ瘑鍥捐氨寮曟搸 - 瀹㈡埛绔煡璇嗗浘璋卞伐鍏凤紝甯姪 AI 浠ｇ悊鐞嗚В浠ｇ爜缁撴瀯銆?
  瑙﹀彂鍦烘櫙锛?
  (1) 鐢ㄦ埛闇€瑕佸垎鏋愰」鐩唬鐮佺粨鏋勩€佷緷璧栧叧绯?
  (2) 鐢ㄦ埛闇€瑕佽拷韪嚱鏁拌皟鐢ㄩ摼
  (3) 鐢ㄦ埛闇€瑕佽瘎浼颁唬鐮佷慨鏀圭殑褰卞搷鑼冨洿
  (4) 鐢ㄦ埛闇€瑕佺悊瑙ｅぇ鍨嬩唬鐮佸簱鐨勬灦鏋?
  (5) 鐢ㄦ埛璇?绱㈠紩椤圭洰"銆?鍒嗘瀽浠ｇ爜"銆?鏌ヨ皟鐢ㄩ摼"銆?褰卞搷鍒嗘瀽"
  鏍稿績鍔熻兘锛氫唬鐮佺储寮曘€佺煡璇嗗浘璋辨瀯寤恒€丮CP 宸ュ叿闆嗘垚锛坬uery/context/impact/rename/cypher锛?
  瀵规瘮 deep-research锛歞eep-research 鏄皟鐮斿閮ㄧ煡璇嗭紝gitnexus 鏄垎鏋愭湰鍦颁唬鐮?
github_url: https://github.com/abhigyanpatwari/GitNexus
github_hash: 8c4197063138abdf3bfb173a811f20df96129725
version: 1.3.2
created_at: 2026-02-21T00:00:00Z
platform: github
source: https://github.com/abhigyanpatwari/GitNexus
stars: 850
language: TypeScript
license: PolyForm Noncommercial
local_only: true
allowed-tools: "Bash Read Glob Grep"
metadata:
  category: code-analysis
  tags:
    - code-analysis
    - knowledge-graph
    - mcp
    - code-indexing
    - static-analysis
---

# GitNexus

瀹㈡埛绔唬鐮佺煡璇嗗浘璋卞紩鎿庯紝灏嗕唬鐮佸簱绱㈠紩涓轰氦浜掑紡鐭ヨ瘑鍥捐氨锛岃 AI 浠ｇ悊姘镐笉閬楁紡浠ｇ爜涓婁笅鏂囥€?

> **瀹樻柟缃戠珯**: https://gitnexus.vercel.app
> **GitHub**: https://github.com/abhigyanpatwari/GitNexus
> **Stars**: 850 | **License**: PolyForm Noncommercial

## 蹇€熷紑濮?

### 瀹夎 CLI

```bash
npm install -g gitnexus
```

楠岃瘉瀹夎锛?

```bash
gitnexus --version
```

### 绱㈠紩椤圭洰

```bash
# 绱㈠紩褰撳墠鐩綍
gitnexus analyze

# 绱㈠紩鎸囧畾鐩綍
gitnexus analyze /path/to/project

# 璺宠繃宓屽叆鐢熸垚锛堝姞蹇储寮曢€熷害锛?
gitnexus analyze --skip-embeddings

# 寮哄埗閲嶅缓绱㈠紩
gitnexus analyze --force
```

### 鍚姩 MCP 鏈嶅姟鍣?

```bash
# 閰嶇疆 MCP锛堢敓鎴?.mcp.json锛?
gitnexus setup

# 鍚姩 MCP 鏈嶅姟鍣?
gitnexus mcp
```

## 鏍稿績鍔熻兘

### 1. 浠ｇ爜绱㈠紩

- 鏀寔 **10+ 缂栫▼璇█**: TypeScript, JavaScript, Python, Java, C, C++, C#, Go, Rust
- 6 闃舵绱㈠紩绠￠亾锛氱粨鏋勫垎鏋?鈫?AST 瑙ｆ瀽 鈫?鍏崇郴瑙ｆ瀽 鈫?鑱氱被 鈫?娴佺▼杩借釜 鈫?鎼滅储
- 鐭ヨ瘑鍥捐氨瀛樺偍鍦ㄩ」鐩?`.gitnexus/` 鐩綍锛堝彲绉绘銆乬itignore锛?

### 2. MCP 宸ュ叿锛? 涓級

| 宸ュ叿 | 鍔熻兘 |
|------|------|
| `list_repos` | 鍙戠幇鎵€鏈夊凡绱㈠紩浠撳簱 |
| `query` | 娣峰悎鎼滅储锛圔M25 + 璇箟 + RRF锛?|
| `context` | 360搴︾鍙疯鍥撅紙瀹氫箟銆佽皟鐢ㄨ€呫€佽璋冪敤鑰呫€佸鍏ワ級 |
| `impact` | 鐖嗙偢鍗婂緞鍒嗘瀽锛堜慨鏀瑰奖鍝嶈寖鍥达級 |
| `detect_changes` | Git 宸紓褰卞搷鍒嗘瀽 |
| `rename` | 澶氭枃浠跺崗璋冮噸鍛藉悕 |
| `cypher` | 鍘熷 Cypher 鍥炬煡璇?|

### 3. Web UI

璁块棶 https://gitnexus.vercel.app 浣跨敤鍙鍖栨祻瑙堝櫒銆?

```bash
# 鏈湴杩愯
git clone https://github.com/abhigyanpatwari/gitnexus.git
cd gitnexus/gitnexus-web
npm install
npm run dev
```

## 浣跨敤绀轰緥

### 鍦烘櫙 1: 鐞嗚В椤圭洰缁撴瀯

```bash
gitnexus analyze
```

鐒跺悗闂?Claude Code锛?
- "杩欎釜椤圭洰鐨勫叆鍙ｇ偣鍦ㄥ摢閲岋紵"
- "涓昏妯″潡鏄浣曠粍缁囩殑锛?

### 鍦烘櫙 2: 杩借釜璋冪敤閾?

闂?Claude Code锛?
- "UserService.login 琚摢浜涘嚱鏁拌皟鐢紵"
- "杩欎釜 API 绔偣鐨勫畬鏁磋皟鐢ㄩ摼鏄粈涔堬紵"

### 鍦烘櫙 3: 褰卞搷鍒嗘瀽

闂?Claude Code锛?
- "濡傛灉淇敼 auth.js锛屼細褰卞搷鍝簺鏂囦欢锛?
- "杩欎釜 API 鐨勬敼鍔ㄤ細褰卞搷鍝簺娑堣垂鑰咃紵"

### 鍦烘櫙 4: 浠ｇ爜鎼滅储

闂?Claude Code锛?
- "鎵惧嚭鎵€鏈変娇鐢?redis 鐨勫湴鏂?
- "鍝噷瀹氫箟浜?handleRequest 鍑芥暟锛?

## 宸ヤ綔鍘熺悊

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                     GitNexus 鏋舵瀯                          鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?  浠ｇ爜杈撳叆 (Git/ZIP) 鈫?绱㈠紩绠￠亾 (6闃舵) 鈫?鐭ヨ瘑鍥捐氨 (KuzuDB)鈹?
鈹?                                             鈹?             鈹?
鈹?        鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?
鈹?        鈻?                                        鈻?       鈹?
鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                          鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹?  鈹? MCP Server 鈹?                          鈹?Web UI  鈹?  鈹?
鈹?  鈹? (7 tools)  鈹?                          鈹?(WASM)  鈹?  鈹?
鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                          鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹?        鈹?                                        鈹?       鈹?
鈹?        鈻?                                        鈻?       鈹?
鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                          鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹?  鈹?AI 浠ｇ悊     鈹?                          鈹?鐭ヨ瘑鍥? 鈹?  鈹?
鈹?  鈹?(Claude/    鈹?                          鈹?鍙鍖? 鈹?  鈹?
鈹?  鈹? Cursor)    鈹?                          鈹?+ Chat  鈹?  鈹?
鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                          鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

## 甯歌闂

### Q: 绱㈠紩寰堟參鎬庝箞鍔烇紵

```bash
# 璺宠繃宓屽叆鐢熸垚
gitnexus analyze --skip-embeddings
```

### Q: Web UI 鍐呭瓨闄愬埗锛?

Web UI 闄愬埗绾?5000 鏂囦欢锛屽ぇ椤圭洰璇蜂娇鐢?CLI + MCP 妯″紡銆?

### Q: MCP 閰嶇疆鍦ㄥ摢閲岋紵

椤圭洰鏍圭洰褰曠殑 `.mcp.json`銆?

### Q: 涓庡叾浠栧伐鍏峰姣旓紵

| 鐗规€?| GitNexus | Sourcegraph | DeepWiki |
|------|----------|-------------|----------|
| 閮ㄧ讲鏂瑰紡 | 瀹㈡埛绔湰鍦?| SaaS/鑷墭绠?| SaaS |
| 鍥捐氨鑳藉姏 | 鉁?鍘熺敓 | 闇€浼佷笟鐗?| 鏈夐檺 |
| MCP 闆嗘垚 | 鉁?鍘熺敓 | 鉂?| 鉂?|
| Token 鏁堢巼 | 楂橈紙棰勮绠楋級 | 涓?| 涓?|
| 闅愮鎬?| 瀹屽叏鏈湴 | 闇€涓婁紶浠ｇ爜 | 闇€涓婁紶浠ｇ爜 |

## 涓庡叾浠?Skills 鐨勯厤鍚?

| Skill | 閰嶅悎鍦烘櫙 |
|-------|----------|
| deep-research | 璋冪爺澶栭儴鎶€鏈?鏂规 |
| omo-skills @explore | 娣卞害浠ｇ爜瀹氫綅 |
| gitnexus | 鍒嗘瀽鏈湴浠ｇ爜缁撴瀯 |

## 璁稿彲璇?

**PolyForm Noncommercial** - 浠呴檺闈炲晢涓氫娇鐢?

---

## 鐗堟湰鍘嗗彶

- **v1.0.0** (2026-02-21): 鍒濆鐗堟湰
  - 浠ｇ爜绱㈠紩鍜屽垎鏋?
  - MCP 宸ュ叿灏佽
  - 褰卞搷鍒嗘瀽鍜岃皟鐢ㄩ摼杩借釜

---

*姝?Skill 鐢?github-to-skills 鑷姩鐢熸垚锛屾敮鎸?skill-manager 鏇存柊妫€鏌?


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 绱㈠紩椤圭洰鏃朵娇鐢?--skip-embeddings 鍔犲揩閫熷害

### Known Fixes & Workarounds
- Skill 鍒涘缓鍚庨渶妫€鏌ユ牴鐩綍鍜?.curated/ 鐩綍鏄惁閮芥湁鍓湰
- scan_and_check.py 鎵弿鏃堕渶瑕佹鏌ユ纭殑鐩綍璺緞

### Custom Instruction Injection

鍒嗘瀽椤圭洰鏃跺厛鎵ц gitnexus analyze 绱㈠紩浠ｇ爜搴