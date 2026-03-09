---
name: academic-writing-suite
description: |
  瀛︽湳鍐欎綔濂椾欢锛氬崗璋?deep-research銆乸aper-search 鍜?pub-figures 瀹屾垚瀛︽湳鍐欎綔浠诲姟锛屾敮鎸?RSS 棰勬壂鎻忚幏鍙栨渶鏂伴鍗版湰銆?
  6 闃舵宸ヤ綔娴侊細RSS 棰勬壂鎻?鈫?闇€姹傚垎鏋?鈫?鏂囩尞璋冪爺 鈫?鎻愮翰璁捐 鈫?鍐呭鎾板啓 鈫?鏁村悎杈撳嚭銆?
  瑙﹀彂鍦烘櫙锛?
  (1) 鐢ㄦ埛闇€瑕佹挵鍐欏鏈鏂囥€佺爺绌舵姤鍛娿€佸熀閲戠敵璇蜂功
  (2) 鐢ㄦ埛璇?鍐欒鏂?銆?鍐欑爺绌舵姤鍛?銆?鍐欏熀閲戠敵璇?
  (3) 闇€瑕佹枃鐚皟鐮?+ 鍥捐〃鐢熸垚 + 鏂囨。杈撳嚭鐨勭患鍚堜换鍔?
  (4) 瀛︽湳鍐欎綔闇€瑕佷笓涓氬浘琛ㄦ敮鎸?
license: MIT
version: 0.2.0
metadata:
  category: research-knowledge
---

# Academic Writing Suite - 瀛︽湳鍐欎綔濂椾欢

鍗忚皟澶氫釜 skill 瀹屾垚瀛︽湳鍐欎綔浠诲姟鐨勭紪鎺掔郴缁熴€?

## 姒傝堪

鏈?skill 鏁村悎浠ヤ笅鑳藉姏锛?
- **rss-reader**: 鏈€鏂伴鍗版湰 RSS 鐩戞帶锛坆ioRxiv銆丳ubMed銆佹湡鍒婏級
- **deep-research**: 绯荤粺鍖栨枃鐚皟鐮旓紙8 姝ユ硶 + 7 杞悳绱級
- **paper-search**: 瀛︽湳鏁版嵁搴撴悳绱紙arXiv銆丳ubMed銆丼emantic Scholar锛?
- **pub-figures**: 鍑虹増绾х瀛﹀浘琛ㄧ敓鎴?

## 閫傜敤鍦烘櫙

| 鍦烘櫙 | 璇存槑 |
|------|------|
| **鐮旂┒鎶ュ憡** | 闇€瑕佹枃鐚敮鎾戠殑鎶€鏈皟鐮旀姤鍛?|
| **瀛︽湳璁烘枃** | 鏈熷垔/浼氳璁烘枃鍐欎綔 |
| **鍩洪噾鐢宠** | 鐮旂┒璁″垝涔︺€侀」鐩敵璇蜂功 |
| **缁艰堪鏂囩珷** | 棰嗗煙缁艰堪銆佹妧鏈櫧鐨功 |
| **瀛︿綅璁烘枃** | 鏈/纭曞＋/鍗氬＋璁烘枃绔犺妭 |

## 5 闃舵宸ヤ綔娴?

### Phase 0: RSS 棰勬壂鎻忥紙鍙€夛紝鎺ㄨ崘锛?

**鐩爣**锛氬湪涓诲姩鎼滅储鍓嶏紝蹇€熻幏鍙栨渶鏂伴鍗版湰鍜屾湡鍒婃枃绔?

**瑙﹀彂鏉′欢**锛氱爺绌朵富棰樻秹鍙婂揩閫熷彂灞曠殑棰嗗煙锛圓I銆佸崟缁嗚優銆佸熀鍥犵粍瀛︾瓑锛?

**鎵ц姝ラ**锛?
1. **鎵弿鐩稿叧 RSS 婧?*
   ```bash
   # 鎵弿 bioRxiv 鐢熶俊棰勫嵃鏈紙鏈€杩?14 澶╋級
   python ~/.claude/skills/.experimental/rss-reader/scripts/rss_fetch.py \
     --source biorxiv --keywords "鍏抽敭璇?,鍏抽敭璇?" --days 14 --max 20

   # 鎵弿 PubMed 鏈€鏂版枃绔?
   python ~/.claude/skills/.experimental/rss-reader/scripts/rss_fetch.py \
     --source pubmed-bioinformatics --keywords "鍏抽敭璇? --days 30 --max 15

   # 鎵弿 medRxiv锛堜复搴婄爺绌讹級
   python ~/.claude/skills/.experimental/rss-reader/scripts/rss_fetch.py \
     --source medrxiv --keywords "鍏抽敭璇? --days 14 --max 10
   ```

2. **绛涢€夐珮鐩稿叧鏂囩珷**
   - 鏍囬鐩存帴鍖归厤鐮旂┒涓婚 鈫?L1 鍊欓€?
   - 鎽樿鍖呭惈鍏抽敭鏂规硶/姒傚康 鈫?L2 鍊欓€?
   - 璁板綍 DOI/URL 渚?Phase 2 娣卞叆妫€绱?

3. **鏇存柊鎼滅储绛栫暐**
   - 鏍规嵁 RSS 缁撴灉璇嗗埆鏈€鏂版湳璇拰鏂规硶鍚嶇О
   - 灏嗘柊鏈鍔犲叆 Phase 2 鐨?paper-search 鍏抽敭璇嶅垪琛?

**杈撳嚭**锛?
- `00_RSS棰勬壂鎻?md` - 鏈€鏂版枃绔犲垪琛紙鏍囬銆佹棩鏈熴€佹憳瑕併€侀摼鎺ワ級
- 鏇存柊鍚庣殑鍏抽敭璇嶅垪琛紙渚?Phase 2 浣跨敤锛?

**璺宠繃鏉′欢**锛?
- 鐮旂┒涓婚鏄巻鍙叉€?缁艰堪鎬э紙涓嶉渶瑕佹渶鏂拌繘灞曪級
- 宸叉湁鍏呰冻鐨勮繎鏈熸枃鐚?

### Phase 1: 闇€姹傚垎鏋?

**鐩爣**锛氭槑纭啓浣滀换鍔＄殑鑼冨洿鍜岃姹?

**鎵ц姝ラ**锛?
1. 纭畾鏂囨。绫诲瀷锛堣鏂?鎶ュ憡/鐢宠涔︼級
2. 鏄庣‘鐩爣鏈熷垔/浼氳/鏈烘瀯鐨勬牸寮忚姹?
3. 纭畾瀛楁暟/椤垫暟闄愬埗
4. 璇嗗埆闇€瑕佺殑鍥捐〃绫诲瀷鍜屾暟閲?
5. 璁惧畾鎴鏃ユ湡鍜岄噷绋嬬

**杈撳嚭**锛?
```markdown
## 鍐欎綔闇€姹傚垎鏋?

- **鏂囨。绫诲瀷**锛歔璁烘枃/鎶ュ憡/鐢宠涔
- **鐩爣鍙戣〃**锛歔鏈熷垔鍚?浼氳鍚?鏈烘瀯]
- **鏍煎紡瑕佹眰**锛歔瀛楁暟/椤垫暟/寮曠敤鏍煎紡]
- **鍥捐〃闇€姹?*锛?
  - [ ] 娴佺▼鍥?鏂规硶鍥?
  - [ ] 鏁版嵁鍥捐〃锛堟煴鐘跺浘/鎶樼嚎鍥?鐑浘锛?
  - [ ] 缁撴灉瀵规瘮琛?
- **鏃堕棿鑺傜偣**锛歔鎴鏃ユ湡]
```

### Phase 2: 鏂囩尞璋冪爺

**鐩爣**锛氭敹闆?40+ 楂樿川閲忓弬鑰冩枃鐚?

**鎵ц姝ラ**锛?

1. **鍚姩 deep-research 璋冪爺**
   - 浣跨敤 8 姝ユ硶杩涜绯荤粺璋冪爺
   - 鎵ц 7 杞悳绱㈢瓥鐣ワ紙鍖呮嫭瀛︽湳鍓嶆部鎼滅储锛?

2. **浣跨敤 paper-search 鎼滅储瀛︽湳鏁版嵁搴?*
   ```bash
   # AI/CS 棰嗗煙
   python ~/.claude/skills/paper-search/scripts/search.py arxiv "<鍏抽敭璇?" --max 20

   # 鐢熺墿鍖诲棰嗗煙
   python ~/.claude/skills/paper-search/scripts/search.py pubmed "<鍏抽敭璇?" --max 20

   # 璺ㄩ鍩熺患鍚?
   python ~/.claude/skills/paper-search/scripts/search.py semantic "<鍏抽敭璇?" --max 20
   ```

3. **鏂囩尞鍒嗙被涓庣瓫閫?*
   - L1 绾у埆锛氭牳蹇冨弬鑰冩枃鐚紙鐩存帴鏀拺璁虹偣锛?
   - L2 绾у埆锛氳儗鏅枃鐚紙鎻愪緵涓婁笅鏂囷級
   - L3 绾у埆锛氳ˉ鍏呮枃鐚紙鎵╁睍闃呰锛?

**杈撳嚭**锛?
- `~/Downloads/research/<topic>/01_璧勬枡鏉ユ簮.md`
- 鑷冲皯 40 绡囧弬鑰冩枃鐚紝鍏朵腑 L1 绾у埆 鈮?15 绡?

### Phase 3: 鎻愮翰璁捐

**鐩爣**锛氳璁℃枃妗ｇ粨鏋勶紝瑙勫垝鍥捐〃浣嶇疆

**鎵ц姝ラ**锛?

1. **纭畾鏂囨。缁撴瀯**
   ```markdown
   # 璁烘枃鎻愮翰

   ## 1. 寮曡█ (Introduction)
   - 鐮旂┒鑳屾櫙
   - 闂闄堣堪
   - 鐮旂┒鐩爣
   - 璐＄尞鎬荤粨

   ## 2. 鐩稿叧宸ヤ綔 (Related Work)
   - 棰嗗煙 A 鐮旂┒鐜扮姸
   - 棰嗗煙 B 鐮旂┒鐜扮姸
   - 鏈枃瀹氫綅

   ## 3. 鏂规硶 (Methods)
   - 鏁翠綋妗嗘灦 [Figure 1: 鏂规硶娴佺▼鍥綸
   - 鏍稿績绠楁硶
   - 瀹炵幇缁嗚妭

   ## 4. 瀹為獙 (Experiments)
   - 瀹為獙璁剧疆 [Table 1: 鏁版嵁闆嗙粺璁
   - 涓昏缁撴灉 [Figure 2: 鎬ц兘瀵规瘮]
   - 娑堣瀺瀹為獙 [Table 2: 娑堣瀺缁撴灉]

   ## 5. 璁ㄨ (Discussion)
   - 缁撴灉鍒嗘瀽
   - 灞€闄愭€?
   - 鏈潵宸ヤ綔

   ## 6. 缁撹 (Conclusion)
   ```

2. **瑙勫垝鍥捐〃**
   - 鏍囪姣忎釜鍥捐〃鐨勪綅缃?
   - 纭畾鍥捐〃绫诲瀷锛堜娇鐢?pub-figures 鏀寔鐨勭被鍨嬶級
   - 鍑嗗鍥捐〃鏁版嵁

**杈撳嚭**锛?
- `outline.md` - 璇︾粏鎻愮翰
- `figures_plan.md` - 鍥捐〃瑙勫垝

### Phase 4: 鍐呭鎾板啓

**鐩爣**锛氬畬鎴愬悇绔犺妭鍐呭 + 鐢熸垚鍥捐〃

**鎵ц姝ラ**锛?

1. **鎸夌珷鑺傛挵鍐?*
   - 浠庢柟娉?瀹為獙绔犺妭寮€濮嬶紙鏈€鍏蜂綋锛?
   - 鐒跺悗鍐欑浉鍏冲伐浣滐紙闇€瑕佹枃鐚敮鎾戯級
   - 鏈€鍚庡啓寮曡█鍜岀粨璁猴紙闇€瑕佸叏灞€瑙嗚锛?

2. **浣跨敤 pub-figures 鐢熸垚鍥捐〃**
   ```python
   # 绀轰緥锛氱敓鎴愬闈㈡澘鍥?
   import matplotlib.pyplot as plt
   from matplotlib.gridspec import GridSpec

   # 搴旂敤鍑虹増绾ч粯璁よ缃?
   plt.rcParams.update({
       'font.family': 'sans-serif',
       'font.sans-serif': ['Arial', 'DejaVu Sans'],
       'savefig.dpi': 600,
   })

   # 鍒涘缓鍥捐〃...
   fig.savefig('Figure_1.pdf', bbox_inches='tight')
   ```

3. **寮曠敤绠＄悊**
   - 浣跨敤涓€鑷寸殑寮曠敤鏍煎紡
   - 纭繚姣忎釜璁虹偣鏈夋枃鐚敮鎾?

**杈撳嚭**锛?
- 鍚勭珷鑺?Markdown 鏂囦欢
- 楂樺垎杈ㄧ巼鍥捐〃锛圥DF + PNG锛?

### Phase 5: 鏁村悎杈撳嚭

**鐩爣**锛氱敓鎴愭渶缁堝彲鎻愪氦鏂囨。

**鎵ц姝ラ**锛?

1. **鏁村悎鎵€鏈夌珷鑺?*
   - 鍚堝苟 Markdown 鏂囦欢
   - 鎻掑叆鍥捐〃
   - 鐢熸垚鍙傝€冩枃鐚垪琛?

2. **鏍煎紡杞崲**锛堟牴鎹洰鏍囨牸寮忥級
   ```bash
   # 杞崲涓?Word
   pandoc paper.md -o paper.docx --reference-doc=template.docx

   # 杞崲涓?LaTeX
   pandoc paper.md -o paper.tex

   # 杞崲涓?PDF
   pandoc paper.md -o paper.pdf --pdf-engine=xelatex
   ```

3. **璐ㄩ噺妫€鏌?*
   - [ ] 鎵€鏈夊浘琛ㄦ竻鏅板彲璇?
   - [ ] 寮曠敤鏍煎紡涓€鑷?
   - [ ] 鏃犳嫾鍐?璇硶閿欒
   - [ ] 绗﹀悎鐩爣鏍煎紡瑕佹眰

**杈撳嚭**锛?
- 鏈€缁堟枃妗ｏ紙.docx / .pdf / .tex锛?
- 鍥捐〃鏂囦欢澶?
- 鍙傝€冩枃鐚枃浠讹紙.bib锛?

## 宸ヤ綔鐩綍缁撴瀯

```
~/Downloads/academic-writing/<project>/
鈹溾攢鈹€ 00_RSS棰勬壂鎻?md          # Phase 0 浜у嚭锛堝彲閫夛級
鈹溾攢鈹€ 00_闇€姹傚垎鏋?md           # Phase 1 浜у嚭
鈹溾攢鈹€ 01_鏂囩尞璋冪爺/             # Phase 2 浜у嚭
鈹?  鈹溾攢鈹€ 璧勬枡鏉ユ簮.md
鈹?  鈹溾攢鈹€ 浜嬪疄鍗＄墖.md
鈹?  鈹斺攢鈹€ papers/              # 涓嬭浇鐨勮鏂?PDF
鈹溾攢鈹€ 02_鎻愮翰/                 # Phase 3 浜у嚭
鈹?  鈹溾攢鈹€ outline.md
鈹?  鈹斺攢鈹€ figures_plan.md
鈹溾攢鈹€ 03_鑽夌/                 # Phase 4 浜у嚭
鈹?  鈹溾攢鈹€ 01_introduction.md
鈹?  鈹溾攢鈹€ 02_related_work.md
鈹?  鈹溾攢鈹€ 03_methods.md
鈹?  鈹溾攢鈹€ 04_experiments.md
鈹?  鈹斺攢鈹€ 05_conclusion.md
鈹溾攢鈹€ 04_鍥捐〃/                 # Phase 4 浜у嚭
鈹?  鈹溾攢鈹€ Figure_1.pdf
鈹?  鈹溾攢鈹€ Figure_1.png
鈹?  鈹斺攢鈹€ ...
鈹溾攢鈹€ 05_杈撳嚭/                 # Phase 5 浜у嚭
鈹?  鈹溾攢鈹€ paper.md
鈹?  鈹溾攢鈹€ paper.docx
鈹?  鈹斺攢鈹€ references.bib
鈹斺攢鈹€ FINAL_璁烘枃.md            # 鏈€缁堢増鏈?
```

## 蹇€熷惎鍔?

浣跨敤 orchestrator 鑴氭湰鍒濆鍖栭」鐩細

```bash
# 鍒濆鍖栭」鐩?
python ~/.claude/skills/academic-writing-suite/scripts/orchestrator.py init "鐮旂┒涓婚"

# 鎵ц鏂囩尞鎼滅储
python ~/.claude/skills/academic-writing-suite/scripts/orchestrator.py search "鍏抽敭璇?

# 鐢熸垚鍥捐〃
python ~/.claude/skills/academic-writing-suite/scripts/orchestrator.py figures

# 鏌ョ湅椤圭洰鐘舵€?
python ~/.claude/skills/academic-writing-suite/scripts/orchestrator.py status
```

## 涓庡叾浠?Skill 鐨勫叧绯?

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                 academic-writing-suite                      鈹?
鈹?                     (缂栨帓灞?                                鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                                                             鈹?
鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?  鈹?rss-reader  鈹? 鈹俤eep-research鈹? 鈹俻aper-search 鈹? 鈹?pub-figures 鈹?
鈹?  鈹? (棰勬壂鎻?   鈹? 鈹? (璋冪爺)     鈹? 鈹? (鎼滅储)     鈹? 鈹? (鍥捐〃)     鈹?
鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?        鈹?               鈹?               鈹?                鈹?
鈹?        鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                鈹?
鈹?                         鈹?                                 鈹?
鈹?                   鈹屸攢鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹?                          鈹?
鈹?                   鈹?  docx    鈹?                          鈹?
鈹?                   鈹? (杈撳嚭)   鈹?                          鈹?
鈹?                   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                          鈹?
鈹?                                                             鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

## 璐ㄩ噺妫€鏌ユ竻鍗?

### 鏂囩尞璋冪爺璐ㄩ噺
- [ ] 鍙傝€冩枃鐚暟閲?鈮?40 绡?
- [ ] L1 绾у埆鏂囩尞 鈮?15 绡?
- [ ] 鍖呭惈杩?2 骞存渶鏂扮爺绌?
- [ ] 瑕嗙洊涓昏鐮旂┒鏂瑰悜

### 鍥捐〃璐ㄩ噺
- [ ] 鍒嗚鲸鐜?鈮?300 DPI
- [ ] 浣跨敤鑹茬洸鍙嬪ソ閰嶈壊
- [ ] 瀛椾綋娓呮櫚鍙
- [ ] 鍥句緥瀹屾暣

### 鍐欎綔璐ㄩ噺
- [ ] 閫昏緫缁撴瀯娓呮櫚
- [ ] 璁虹偣鏈夋枃鐚敮鎾?
- [ ] 鏃犳妱琚?杩囧害寮曠敤
- [ ] 璇█娴佺晠鍑嗙‘

## 鐗堟湰鍘嗗彶

- **v0.2.0** (2026-02-26): 娣诲姞 Phase 0 RSS 棰勬壂鎻?
  - 闆嗘垚 rss-reader skill
  - 鏀寔 bioRxiv/PubMed/medRxiv 棰勫嵃鏈洃鎺?
- **v1.0** (2026-01-28): 鍒濆鐗堟湰
  - 鏁村悎 deep-research銆乸aper-search銆乸ub-figures
  - 5 闃舵宸ヤ綔娴?
  - orchestrator 鑴氭湰鏀寔

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 项目目录默认创建在 ~/Downloads/academic-writing/ 下
- orchestrator.py 的 init 命令会自动创建 5 阶段子目录

### Known Fixes & Workarounds
- Windows 路径需要使用 Path 对象处理，避免编码问题
- 中文目录名在 Windows 终端显示可能乱码，但实际创建正确

### Custom Instruction Injection

创建新 skill 时，确保 name 字段使用 kebab-case 格式并与文件夹名一致