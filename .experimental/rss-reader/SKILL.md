---
name: rss-reader
description: 璁㈤槄鍜岃繃婊ゅ鏈?RSS 婧愶紝鐩戞帶棰勫嵃鏈湇鍔″櫒鍜屾湡鍒婃洿鏂般€傝Е鍙戝満鏅細璁㈤槄RSS銆佺洃鎺ч鍗版湰銆佹枃鐚拷韪€佹渶鏂拌鏂囥€乺ss銆乫eed
version: 1.0.0
allowed-tools:
  - Bash(python:*)
metadata:
  category: research-knowledge
---

# RSS Reader Skill

瀛︽湳 RSS 璁㈤槄涓庤繃婊ゅ伐鍏凤紝鐢ㄤ簬杩借釜 bioRxiv銆丳ubMed銆丯ature 绛夊鏈簮鐨勬渶鏂版枃鐚€?

## 瑙﹀彂璇?

- 璁㈤槄RSS / 璁㈤槄 RSS
- 鐩戞帶棰勫嵃鏈?
- 鏂囩尞杩借釜
- 鏈€鏂拌鏂?
- rss / feed

## 鏀寔鐨勫鏈?RSS 婧?

| 鍚嶇О | 鏉＄洰鏁?| 璇存槑 |
|------|--------|------|
| `biorxiv` | ~30 | bioRxiv 鐢熺墿淇℃伅瀛﹂鍗版湰 |
| `biorxiv-all` | ~30 | bioRxiv 鍏ㄩ儴瀛︾棰勫嵃鏈?|
| `medrxiv` | ~30 | medRxiv 涓村簥鍖诲棰勫嵃鏈?|
| `nature` | ~75 | Nature 鏈熷垔 |
| `cell` | ~19 | Cell 鏈熷垔 |
| `science` | ~10 | Science 鏈熷垔鏂伴椈 |
| `nejm` | ~35 | New England Journal of Medicine |
| `pnas` | ~107 | PNAS |
| `elife` | ~100 | eLife |

> **娉ㄦ剰**锛歅ubMed RSS 闇€瑕佺櫥褰曪紝鏃犳硶鐩存帴璁㈤槄銆侾ubMed 鏂囩尞妫€绱㈣浣跨敤 `paper-search` skill銆?

## 浣跨敤鏂瑰紡

### 鍩烘湰鐢ㄦ硶

```bash
python ~/.claude/skills/.experimental/rss-reader/scripts/rss_fetch.py --source biorxiv
```

### 鎸夊叧閿瘝杩囨护

```bash
python ~/.claude/skills/.experimental/rss-reader/scripts/rss_fetch.py \
  --source pubmed-bioinformatics \
  --keywords "single cell,RNA-seq" \
  --days 7 \
  --max 10
```

### 浣跨敤鑷畾涔?URL

```bash
python ~/.claude/skills/.experimental/rss-reader/scripts/rss_fetch.py \
  --feed "https://www.biorxiv.org/rss/subject/genomics" \
  --keywords "CRISPR" \
  --output json
```

### 杈撳嚭鏍煎紡

- `text`锛堥粯璁わ級锛氭瘡鏉℃枃绔犳樉绀烘爣棰樸€佷綔鑰呫€佹棩鏈熴€佹憳瑕佸墠200瀛椼€侀摼鎺?
- `json`锛氬畬鏁寸粨鏋勫寲 JSON锛岄€傚悎绋嬪簭澶勭悊

## 渚濊禆瀹夎

```bash
pip install feedparser
```

## 涓庡叾浠?Skill 闆嗘垚

### 涓?paper-search 闆嗘垚

RSS 鍙戠幇鎰熷叴瓒ｇ殑璁烘枃鍚庯紝鍙敤 `paper-search` 涓嬭浇鍏ㄦ枃锛?

```
/paper-search 涓嬭浇 [璁烘枃鏍囬鎴?DOI]
```

### 涓?academic-writing-suite 闆嗘垚

`academic-writing-suite` 鐨?RSS 棰勬壂鎻忛樁娈典細鑷姩璋冪敤鏈?skill锛?
鑾峰彇鏈€鏂伴鍗版湰浣滀负鍐欎綔鍙傝€冦€備篃鍙墜鍔ㄨЕ鍙戯細

```
鍏堢敤 rss-reader 鑾峰彇鏈€鏂?biorxiv 鏂囩珷锛屽叧閿瘝 "transformer protein"锛?
鐒跺悗鐢?academic-writing-suite 鍐欑患杩?
```

## 绀轰緥瀵硅瘽

**鐢ㄦ埛**锛氬府鎴戣拷韪?bioRxiv 涓婃渶杩?澶╁叧浜?single-cell 鐨勯鍗版湰

**鎵ц**锛?
```bash
python ~/.claude/skills/.experimental/rss-reader/scripts/rss_fetch.py \
  --source biorxiv-all \
  --keywords "single-cell,scRNA-seq,single cell" \
  --days 7 \
  --max 20
```

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 浼樺厛浣跨敤宸查獙璇佺殑婧愶紙biorxiv, biorxiv-all, medrxiv, nature, cell, science, nejm, pnas, elife锛?
- PubMed 鏌ヨ缁熶竴璧?`paper-search` skill锛屼笉璧?RSS

### Known Fixes & Workarounds
- **bioRxiv 姝ｇ‘ URL**锛歚www.biorxiv.org/rss/subject/bioinformatics` 杩斿洖 403锛屽簲浣跨敤 `connect.biorxiv.org/biorxiv_xml.php?subject=bioinformatics`
- **medRxiv 姝ｇ‘ URL**锛歚connect.biorxiv.org/medrxiv_xml.php` 杩斿洖 404锛屽簲浣跨敤 `connect.medrxiv.org/medrxiv_xml.php?subject=all`
- **PubMed RSS 涓嶅彲鐢?*锛歅ubMed RSS 闇€瑕佺櫥褰曪紝杩斿洖 HTML 椤甸潰鑰岄潪 RSS锛宖eedparser 瑙ｆ瀽澶辫触锛涘簲浣跨敤 `paper-search` skill 鏇夸唬
- **Cell 姝ｇ‘ URL**锛歚www.cell.com/cell/rss` 杩斿洖 403锛屽簲浣跨敤 `www.cell.com/cell/current.rss`
- **Windows GBK 缂栫爜闂**锛氬湪杈撳嚭鍓嶉渶鍔?`sys.stdout.reconfigure(encoding='utf-8', errors='replace')` 閬垮厤 GBK 缂栫爜閿欒
- **feedparser bozo=True 涓嶄唬琛ㄦ棤鏁版嵁**锛歟Life 绛夋簮 bozo=True 浣嗕粛鏈?entries锛屼笉搴斿洜 bozo 璺宠繃瑙ｆ瀽锛屽簲缁х画澶勭悊 entries
