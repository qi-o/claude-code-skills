# Research to Diagram - 浣跨敤鎸囧崡

浠庣爺绌跺埌鍙鍖栫殑涓€绔欏紡鐭ヨ瘑鍥捐氨鐢熸垚宸ュ叿銆?

## 蹇€熷紑濮?

### 1. 瀹夎渚濊禆

```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# 楠岃瘉瀹夎
dot -V
```

### 2. 浣跨敤 Skill

鐩存帴鍚?Claude Code 鎻忚堪浣犵殑鐮旂┒闇€姹傦細

```bash
# 绀轰緥 1锛氭枃瀛︿綔鍝佷汉鐗╁叧绯?
"娣卞害璋冩煡銆婄孩妤兼ⅵ銆嬮噷浜虹墿涔嬮棿鐨勫叧绯伙紝鐒跺悗鍋氫釜缁撴瀯鍥?PDF"

# 绀轰緥 2锛氭妧鏈灦鏋勭爺绌?
"鐮旂┒ Kubernetes 鐨勬灦鏋勫苟鐢熸垚鍙鍖栧浘璋?

# 绀轰緥 3锛氬巻鍙蹭簨浠跺垎鏋?
"鍒嗘瀽鏄ョ鎴樺浗鏃舵湡鍚勫浗鍏崇郴锛屽仛鎴愬叧绯诲浘"
```

## 宸ヤ綔娴佺▼

```
鐢ㄦ埛杈撳叆涓婚
    鈫?
WebSearch 娣卞害璋冪爺
    鈫?
淇℃伅鎻愬彇涓庢暣鐞?
    鈫?
缁撴瀯璁捐
    鈫?
鐢熸垚 Graphviz DOT
    鈫?
缂栬瘧涓?PDF
    鈫?
鎻愪緵涓嬭浇閾炬帴鍜屽弬鑰冭祫鏂?
```

## 妯℃澘绀轰緥

### 浜虹墿鍏崇郴鍥?

閫傜敤鍦烘櫙锛?
- 鏂囧浣滃搧浜虹墿鍒嗘瀽
- 鍘嗗彶浜虹墿鍏崇郴
- 瀹舵棌璋辩郴
- 缁勭粐浜哄憳缁撴瀯

鍙傝€冩ā鏉匡細`examples/character_relationships.dot`

鐗圭偣锛?
- 浣跨敤 `cluster` 鍒嗙粍瀹舵棌/鍥綋
- 涓嶅悓棰滆壊鍖哄垎绫诲埆
- 绾㈣壊瀹炵嚎琛ㄧず濠氬Щ锛岄粦鑹茶〃绀鸿缂?
- 铏氱嚎琛ㄧず鍏朵粬鍏崇郴

### 姒傚康鍥捐氨

閫傜敤鍦烘櫙锛?
- 鐭ヨ瘑浣撶郴姊崇悊
- 瀛︾鍒嗙被
- 姒傚康鍏崇郴鍒嗘瀽
- 鎬濈淮瀵煎浘

鍙傝€冩ā鏉匡細`examples/concept_map.dot`

鐗圭偣锛?
- 鏍戠姸灞傛缁撴瀯
- 鏍稿績姒傚康鍦ㄩ《閮?
- 棰滆壊缂栫爜涓嶅悓绫诲埆
- 铏氱嚎琛ㄧず鍏宠仈鍏崇郴

### 鎶€鏈灦鏋勫浘

閫傜敤鍦烘櫙锛?
- 绯荤粺鏋舵瀯璁捐
- 寰湇鍔℃灦鏋?
- 鎶€鏈爤鍙鍖?
- 缁勪欢渚濊禆鍏崇郴

鍙傝€冩ā鏉匡細`examples/tech_architecture.dot`

鐗圭偣锛?
- 鍒嗗眰鏋舵瀯锛堝鎴风/缃戝叧/搴旂敤/鏁版嵁锛?
- 涓嶅悓褰㈢姸琛ㄧず涓嶅悓缁勪欢绫诲瀷
- 瀹炵嚎=鍚屾璋冪敤锛岃櫄绾?寮傛
- 鍖呭惈鍥句緥璇存槑

## 鎵嬪姩鐢熸垚 PDF

濡傛灉浣犳湁 `.dot` 鏂囦欢锛屽彲浠ヤ娇鐢ㄦ彁渚涚殑鑴氭湰鐢熸垚 PDF锛?

```bash
# 浣跨敤鑴氭湰
bash ~/.claude/skills/research-to-diagram/scripts/generate_pdf.sh input.dot output.pdf

# 鎴栫洿鎺ヤ娇鐢?dot 鍛戒护
dot -Tpdf input.dot -o output.pdf

# 鐢熸垚鍏朵粬鏍煎紡
dot -Tpng input.dot -o output.png  # PNG 鍥剧墖
dot -Tsvg input.dot -o output.svg  # SVG 鐭㈤噺鍥?
```

## Graphviz 甯哥敤閰嶇疆

### 甯冨眬鏂瑰悜

```dot
graph [rankdir=TB]  // 涓婂埌涓?
graph [rankdir=LR]  // 宸﹀埌鍙?
graph [rankdir=BT]  // 涓嬪埌涓?
graph [rankdir=RL]  // 鍙冲埌宸?
```

### 鑺傜偣褰㈢姸

```dot
node [shape=box]        // 鐭╁舰
node [shape=ellipse]    // 妞渾
node [shape=circle]     // 鍦嗗舰
node [shape=diamond]    // 鑿卞舰
node [shape=cylinder]   // 鏌辩姸锛堟暟鎹簱锛?
node [shape=component]  // 缁勪欢
```

### 杈圭殑鏍峰紡

```dot
edge [style=solid]      // 瀹炵嚎
edge [style=dashed]     // 铏氱嚎
edge [style=dotted]     // 鐐圭嚎
edge [style=bold]       // 绮楃嚎
edge [arrowsize=0.8]    // 绠ご澶у皬
```

### 涓枃鏀寔

```dot
graph [fontname="Arial Unicode MS"]
node [fontname="Arial Unicode MS"]
edge [fontname="Arial Unicode MS"]

// 鎴栦娇鐢ㄧ郴缁熷瓧浣?
graph [fontname="STHeiti"]  // macOS 榛戜綋
graph [fontname="SimHei"]   // Windows 榛戜綋
```

### 棰滆壊鏂规

甯哥敤棰滆壊锛?
- `#ffd700` - 閲戣壊锛堥噸瑕侊級
- `#ff6347` - 鐣寗绾紙涓昏锛?
- `#87ceeb` - 澶╄摑鑹诧紙娆¤锛?
- `#98fb98` - 娣＄豢鑹诧紙杈呭姪锛?
- `#ffb6c1` - 绮夌孩锛堢壒娈婏級

棰滆壊鍛藉悕锛?
- `red`, `blue`, `green`, `yellow`, `purple`, `orange`
- `lightgrey`, `lightblue`, `lightgreen`

## 楂樼骇鎶€宸?

### 1. 寮哄埗鑺傜偣鍚屽眰

```dot
{rank=same; node1; node2; node3}
```

### 2. 闅愯棌杈癸紙鎺у埗甯冨眬锛?

```dot
node1 -> node2 [style=invis]
```

### 3. 鍚堝苟鐩稿悓杈?

```dot
graph [concentrate=true]
```

### 4. 璋冩暣闂磋窛

```dot
graph [
    nodesep=1.0    // 鑺傜偣姘村钩闂磋窛
    ranksep=1.5    // 灞傜骇鍨傜洿闂磋窛
]
```

### 5. 璺?cluster 杩炴帴

```dot
graph [compound=true]
node1 -> node2 [ltail=cluster_a lhead=cluster_b]
```

## 甯歌闂

### Q: 涓枃鏄剧ず涓轰贡鐮佹垨鏂规

A: 纭繚璁剧疆浜嗕腑鏂囧瓧浣擄細

```dot
graph [fontname="Arial Unicode MS"]
node [fontname="Arial Unicode MS"]
edge [fontname="Arial Unicode MS"]
```

### Q: 鍥捐氨澶鏉傦紝甯冨眬娣蜂贡

A:
1. 浣跨敤 `concentrate=true` 鍚堝苟杈?
2. 璋冩暣 `nodesep` 鍜?`ranksep` 澧炲ぇ闂磋窛
3. 鍒嗗壊鎴愬涓瓙鍥?
4. 浣跨敤 `rank=same` 鎺у埗甯冨眬

### Q: 杈圭殑鏍囩閲嶅彔

A:
1. 鍑忓皯鏍囩闀垮害
2. 浣跨敤 `labeldistance` 鍜?`labelangle` 璋冩暣浣嶇疆
3. 鏀圭敤 `xlabel` 浠ｆ浛 `label`

### Q: PDF 鏂囦欢澶ぇ

A:
1. 浣跨敤 SVG 鏍煎紡锛歚dot -Tsvg input.dot -o output.svg`
2. 鍑忓皯鑺傜偣鏁伴噺锛屾彁楂樻娊璞″眰娆?
3. 鍒嗗壊鎴愬涓浘琛?

### Q: 鎯宠姘村钩甯冨眬

A: 灏?`rankdir=TB` 鏀逛负 `rankdir=LR`

## 鍙傝€冭祫婧?

- [Graphviz 瀹樻柟鏂囨。](https://graphviz.org/documentation/)
- [DOT 璇█鎸囧崡](https://graphviz.org/doc/info/lang.html)
- [鑺傜偣褰㈢姸鍙傝€僝(https://graphviz.org/doc/info/shapes.html)
- [棰滆壊鍚嶇О鍒楄〃](https://graphviz.org/doc/info/colors.html)

## 涓?structure-to-pdf 鐨勫姣?

| 鐗规€?| research-to-diagram | structure-to-pdf |
|------|---------------------|------------------|
| **鏁版嵁鏉ユ簮** | 鑷姩璋冪爺鏀堕泦 | 鐢ㄦ埛鎻愪緵 |
| **閫傜敤鍦烘櫙** | 鎺㈢储鎬х爺绌?| 蹇€熻浆鎹?|
| **璋冪爺鑳藉姏** | 鉁?WebSearch | 鉂?|
| **鐭ヨ瘑鏁寸悊** | 鉁?鑷姩鎻愬彇 | 鉂?|
| **宸ヤ綔閲?* | 鍏ㄨ嚜鍔?| 闇€鍑嗗鏁版嵁 |
| **鏃堕棿** | 杈冮暱锛?-5鍒嗛挓锛?| 蹇€燂紙<1鍒嗛挓锛?|
| **鍙傝€冭祫鏂?* | 鉁?鎻愪緵鏉ユ簮 | 鉂?|
| **閫傚悎涓婚** | 澶嶆潅鐭ヨ瘑浣撶郴 | 绠€鍗曠粨鏋勬暟鎹?|

**閫夋嫨寤鸿**锛?
- 馃摎 **鐮旂┒鍨嬩换鍔?* 鈫?浣跨敤 `research-to-diagram`
- 馃攧 **杞崲鍨嬩换鍔?* 鈫?浣跨敤 `structure-to-pdf`

## 绀轰緥椤圭洰

### 1. 绾㈡ゼ姊︿汉鐗╁叧绯诲浘

**杈撳叆**锛?
```
娣卞害璋冩煡銆婄孩妤兼ⅵ銆嬮噷浜虹墿涔嬮棿鐨勫叧绯伙紝鐒跺悗鍋氫釜缁撴瀯鍥?PDF
```

**杈撳嚭**锛?
- `hongloumeng_relations.dot` - 婧愭枃浠?
- `hongloumeng_relations.pdf` - 152KB PDF
- 鍖呭惈鍥涘ぇ瀹舵棌銆侀噾闄靛崄浜岄挆銆佸疂榛涢挆涓夎鍏崇郴

**鐗硅壊**锛?
- 7涓?subgraph cluster 鍒嗙粍
- 50+ 浜虹墿鑺傜偣
- 澶氱鍏崇郴绫诲瀷锛堣缂樸€佸濮汇€佽仈濮伙級
- 瀹屾暣鍥句緥璇存槑

### 2. Kubernetes 鏋舵瀯鍥?

**杈撳叆**锛?
```
鐮旂┒ Kubernetes 鏋舵瀯骞剁敓鎴愬彲瑙嗗寲鍥捐氨
```

**鍙兘杈撳嚭**锛?
- 鎺у埗骞抽潰缁勪欢锛圓PI Server, Scheduler, Controller Manager锛?
- 鏁版嵁骞抽潰缁勪欢锛圞ubelet, Kube-proxy锛?
- 鎻掍欢鐢熸€侊紙CNI, CSI, CRI锛?
- 缁勪欢闂撮€氫俊鍏崇郴

### 3. 涓夊浗浜虹墿鍏崇郴

**杈撳叆**锛?
```
鍒嗘瀽銆婁笁鍥芥紨涔夈€嬩富瑕佷汉鐗╁叧绯伙紝鐢熸垚鍏崇郴鍥?
```

**鍙兘杈撳嚭**锛?
- 榄忚渶鍚翠笁澶ч樀钀?
- 鍚涜嚕鍏崇郴銆佸厔寮熷叧绯汇€佽仈鐩熷叧绯?
- 閲嶈鎴樺焦鑺傜偣
- 浜虹墿鍛借繍璧板悜

## 鐗堟湰鍘嗗彶

- **v1.0** (2026-01-02)
  - 鍒濆鍙戝竷
  - 鍩轰簬绾㈡ゼ姊︿汉鐗╁叧绯诲浘椤圭洰缁忛獙
  - 鏀寔 Graphviz/DOT 鑷姩鐢熸垚
  - 闆嗘垚 WebSearch 娣卞害璋冪爺
  - 鎻愪緵涓夌妯℃澘锛堜汉鐗?姒傚康/鎶€鏈級

## 璐＄尞

娆㈣繋鎻愪氦锛?
- 鏂扮殑鍥捐氨妯℃澘
- 鏈€浣冲疄璺垫渚?
- Bug 鎶ュ憡
- 鍔熻兘寤鸿

## 璁稿彲璇?

MIT License
