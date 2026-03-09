---
name: deep-research
description: |
  娣卞害璋冪爺鏂规硶璁猴紙8姝ユ硶锛夛細灏嗘ā绯婁富棰樿浆鍖栦负楂樿川閲忚皟鐮旀姤鍛娿€?
  鑷姩鎵ц闂鎷嗚В銆佽祫鏂欏垎灞傘€佷簨瀹炴娊鍙栥€佹鏋跺姣斻€佹帹瀵奸獙璇侊紝杈撳嚭鍙氦浠樼殑缁撴瀯鍖栨姤鍛娿€?
  瑙﹀彂璇嶏細
  - "娣卞害璋冪爺"銆?娣卞害鐮旂┒"銆?娣卞叆鍒嗘瀽"
  - "甯垜璋冪爺"銆?璋冪爺涓€涓?銆?鐮旂┒涓€涓?
  - "瀵规瘮鍒嗘瀽"銆?姒傚康瀵规瘮"銆?鎶€鏈姣?
  - "鍐欒皟鐮旀姤鍛?銆?鍑鸿皟鐮旀姤鍛?
  娉ㄦ剰锛氬鏋滅敤鎴烽渶瑕佺殑鏄彲瑙嗗寲鍥捐氨鑰岄潪鎶ュ憡锛岃浣跨敤 research-to-diagram skill銆?
  Do NOT use for simple factual questions or quick lookups (use WebSearch or ducksearch instead).
github_url: https://github.com/wshuyi/deep-research
github_hash: 8711b7678fc7cc3f1aacf70100ec3a9d6ceccbc4
license: MIT
allowed-tools: "WebSearch WebFetch Read Write Edit"
version: 1.0.0
metadata:
  category: research-knowledge
---

# Deep Research锛堟繁搴﹁皟鐮?8 姝ユ硶锛?

灏嗙敤鎴锋彁鍑虹殑妯＄硦涓婚锛岄€氳繃绯荤粺鍖栨柟娉曡浆鍖栦负楂樿川閲忋€佸彲浜や粯鐨勮皟鐮旀姤鍛娿€?

> 璇︾粏鏂规硶璁恒€佹ā鏉垮拰妫€鏌ユ竻鍗曡 [references/methodology.md](references/methodology.md)

## 鏍稿績鐞嗗康

- **缁撹鏉ヨ嚜鏈哄埗瀵规瘮锛屼笉鏄?鎴戞劅瑙夊儚"**
- **鍏堥拤鐗簨瀹烇紝鍐嶅仛鎺ㄥ**
- **璧勬枡鏉冨▉浼樺厛锛孡1 > L2 > L3 > L4**
- **涓棿缁撴灉蹇呴』淇濆瓨锛屼究浜庡洖婧拰澶嶇敤**

## 宸ヤ綔鐩綍缁撴瀯

璋冪爺寮€濮嬫椂锛?*蹇呴』**鍦?`~/Downloads/research/` 涓嬪垱寤轰互涓婚鍛藉悕鐨勫伐浣滅洰褰曪細

```
~/Downloads/research/<topic>/
鈹溾攢鈹€ 00_闂鎷嗚В.md          # Step 0-1 浜у嚭
鈹溾攢鈹€ 01_璧勬枡鏉ユ簮.md          # Step 2 浜у嚭
鈹溾攢鈹€ 02_浜嬪疄鍗＄墖.md          # Step 3 浜у嚭
鈹溾攢鈹€ 03_瀵规瘮妗嗘灦.md          # Step 4 浜у嚭
鈹溾攢鈹€ 04_鎺ㄥ杩囩▼.md          # Step 6 浜у嚭
鈹溾攢鈹€ 05_楠岃瘉璁板綍.md          # Step 7 浜у嚭
鈹溾攢鈹€ FINAL_璋冪爺鎶ュ憡.md       # Step 8 浜у嚭
鈹斺攢鈹€ raw/                    # 鍘熷璧勬枡瀛樻。锛堝彲閫夛級
```

## Workflow锛? 姝ユ硶锛?

| 姝ラ | 鍚嶇О | 鏍稿績浠诲姟 | 浜у嚭鏂囦欢 |
|------|------|----------|----------|
| **0** | 闂绫诲瀷鍒ゆ柇 | 姒傚康瀵规瘮/鍐崇瓥鏀寔/瓒嬪娍鍒嗘瀽/闂璇婃柇/鐭ヨ瘑姊崇悊 | `00_闂鎷嗚В.md` |
| **0.5** | 鏃舵晥鏁忔劅鎬у垽鏂?| 馃敶鏋侀珮/馃煚楂?馃煛涓?馃煝浣庯紝鍐冲畾璧勬枡鏃堕棿绐楀彛 | 杩藉姞鍒?`00_闂鎷嗚В.md` |
| **1** | 闂鎷嗚В | 鎷嗘垚 2-4 涓瓙闂锛屾槑纭爺绌惰竟鐣岋紙浜虹兢/鍦板煙/鏃堕棿/灞傜骇锛?| `00_闂鎷嗚В.md` |
| **2** | 璧勬枡鍒嗗眰 | L1瀹樻柟>L2鍗氬>L3濯掍綋>L4绀惧尯锛?杞悳绱㈢瓥鐣?| `01_璧勬枡鏉ユ簮.md` |
| **3** | 浜嬪疄鎶藉彇 | 鍙牳楠屼簨瀹炲崱鐗囷紝鏍囨敞鍑哄鍜岀疆淇″害 | `02_浜嬪疄鍗＄墖.md` |
| **4** | 寤虹珛妗嗘灦 | 鍥哄畾缁村害锛岀粨鏋勫寲瀵规瘮 | `03_瀵规瘮妗嗘灦.md` |
| **5** | 鍙傜収鐗╁榻?| 纭繚瀹氫箟缁熶竴 | 鈥?|
| **6** | 鎺ㄥ閾?| 浜嬪疄鈫掑鐓р啋缁撹锛屾樉寮忓啓鍑?| `04_鎺ㄥ杩囩▼.md` |
| **7** | 鐢ㄤ緥楠岃瘉 | Sanity check锛岄槻姝㈢焊涓婅皥鍏?| `05_楠岃瘉璁板綍.md` |
| **8** | 浜や粯鍖?| 涓€鍙ヨ瘽鎬荤粨 + 缁撴瀯鍖栫珷鑺?+ 璇佹嵁鍙拷婧?| `FINAL_璋冪爺鎶ュ憡.md` |

**姣忓畬鎴愪竴涓楠わ紝绔嬪嵆鍐欏叆瀵瑰簲鏂囦欢锛屼笉瑕佺瓑鍒版渶鍚庛€?*

## 璧勬枡鍒嗗眰閫熸煡

| 灞傜骇 | 璧勬枡绫诲瀷 | 鍙俊搴?|
|------|----------|--------|
| **L1** | 瀹樻柟鏂囨。銆佽鏂囥€佽鑼冦€丷FC | 鉁?楂?|
| **L2** | 瀹樻柟鍗氬銆佹妧鏈紨璁层€佺櫧鐨功 | 鉁?楂?|
| **L3** | 鏉冨▉濯掍綋銆佷笓瀹惰В璇汇€佹暀绋?| 鈿狅笍 涓?|
| **L4** | 绀惧尯璁ㄨ銆佷釜浜哄崥瀹€佽鍧?| 鉂?浣?|

缁撹蹇呴』鑳借拷婧埌 L1/L2锛孡3/L4 鍙綔杈呭姪鍜岄獙璇併€?

## 鎶ュ憡杈撳嚭缁撴瀯

```markdown
# [璋冪爺涓婚] 璋冪爺鎶ュ憡

## 鎽樿
[涓€鍙ヨ瘽鎬荤粨鏍稿績缁撹]

## 1. 姒傚康瀵归綈
## 2. 宸ヤ綔鏈哄埗
## 3. 鑱旂郴
## 4. 鍖哄埆
## 5. 鐢ㄤ緥婕旂ず
## 6. 鎬荤粨涓庡缓璁?
## 鍙傝€冭祫鏂?
```

## 鎵撳寘杈撳嚭锛圔LOCKING锛?

```bash
tar -czvf ~/outcome.tar.gz -C <parent_dir> <workspace_name>
```

## 鏈€缁堝洖澶嶈鑼?

**搴斿寘鍚?*锛氫竴鍙ヨ瘽鏍稿績缁撹銆佸叧閿彂鐜版憳瑕侊紙3-5 鐐癸級銆佹墦鍖呮枃浠朵綅缃?
**绂佹鍖呭惈**锛氳繃绋嬫枃浠跺垪琛ㄣ€佽缁嗚皟鐮旀楠よ鏄庛€佸伐浣滅洰褰曠粨鏋勫睍绀?

## 鏂规硶璁洪€熸煡鍗?

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                   娣卞害璋冪爺 8 姝ユ硶                           鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?0. 鍒ゆ柇闂绫诲瀷 鈫?閫夋嫨瀵瑰簲妗嗘灦妯℃澘                            鈹?
鈹?1. 闂鎷嗚В 鈫?2-4 涓彲璋冪爺瀛愰棶棰?                            鈹?
鈹?2. 璧勬枡鍒嗗眰 鈫?L1瀹樻柟 > L2鍗氬 > L3濯掍綋 > L4绀惧尯              鈹?
鈹?3. 浜嬪疄鎶藉彇 鈫?姣忔潯甯﹀嚭澶勩€佹爣缃俊搴?                           鈹?
鈹?4. 寤虹珛妗嗘灦 鈫?鍥哄畾缁村害锛岀粨鏋勫寲瀵规瘮                            鈹?
鈹?5. 鍙傜収鐗╁榻?鈫?纭繚瀹氫箟缁熶竴                                  鈹?
鈹?6. 鎺ㄥ閾?鈫?浜嬪疄鈫掑鐓р啋缁撹锛屾樉寮忓啓鍑?                         鈹?
鈹?7. 鐢ㄤ緥楠岃瘉 鈫?Sanity check锛岄槻姝㈢焊涓婅皥鍏?                    鈹?
鈹?8. 浜や粯鍖?鈫?涓€鍙ヨ瘽鎬荤粨 + 缁撴瀯鍖栫珷鑺?+ 璇佹嵁鍙拷婧?             鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?鎶ュ憡缁撴瀯锛氬畾涔夆啋鏈哄埗鈫掕仈绯烩啋鍖哄埆鈫掔敤渚嬧啋鎬荤粨                       鈹?
鈹?鍏抽敭绾緥锛氱粨璁烘潵鑷満鍒跺姣旓紝涓嶆槸"鎴戞劅瑙夊儚"                     鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 学术调研时自动触发第七轮学术前沿搜索
- 学术资料自动归类为 L1 级别
- Chinese regulatory/policy research should default to WebSearch over WebFetch, as Chinese government domains (cac.gov.cn, nhc.gov.cn, news.cn, chinanews.com.cn) consistently block WebFetch
- When researching Chinese social phenomena, search across multiple source types: official notices, media investigations, enforcement data, academic frameworks
- SKILL.md 体积控制在 150 行 / 5000 字符以内，超出部分使用 references/ 目录的渐进式加载

### Known Fixes & Workarounds
- paper-search 脚本路径在 Windows 上需要使用完整路径
- WebFetch returns 'Unable to verify if domain is safe' for Chinese .gov.cn and .cn domains; use WebSearch summaries instead
- For topic_only blog tasks, research agent should aim for 12-15 cards minimum to reach saturation threshold
- SKILL.md 超过 5000 词时必须拆分到 references/ 目录，核心文件保留流程概览和速查表，详细方法论移至 references/methodology.md
- 拆分后 SKILL.md 必须包含指向 references/ 的链接，格式：> 详细方法论见 [references/methodology.md](references/methodology.md)
- WebFetch 被阻断时立即切换 ducksearch skill（DuckDuckGo），不要继续重试 WebFetch；web-research 依赖 gemini-search agent，当前环境不可用，禁止调用

### Custom Instruction Injection

涉及科学原理、算法、技术机制的调研必须执行学术搜索轮次