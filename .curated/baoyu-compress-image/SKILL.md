---
name: baoyu-compress-image
version: 1.8.0description: |
  鍥剧墖鍘嬬缉宸ュ叿銆傚皢鍥剧墖鍘嬬缉涓?WebP锛堥粯璁わ級鎴?PNG/JPEG 鏍煎紡锛岃嚜鍔ㄩ€夋嫨鏈€浣冲帇缂╁伐鍏枫€?
  鏀寔鍗曟枃浠跺拰鎵归噺鐩綍澶勭悊銆?
  瑙﹀彂璇嶏細鍘嬬缉鍥剧墖銆乧ompress image銆佸浘鐗囦紭鍖栥€乺educe image size
github_url: https://github.com/JimLiu/baoyu-skills
github_hash: 51443359169ce3bfab458083f1212a5d83317aa8
source: skills/baoyu-compress-image
license: MIT
allowed-tools: "Bash(cwebp:*) Bash(python:*) Read"
metadata:
  category: media-tools
---

# Baoyu Compress Image

鍥剧墖鍘嬬缉宸ュ叿锛屾敮鎸佸绉嶆牸寮忓拰鎵归噺澶勭悊銆?

## 鏍稿績鍔熻兘

- 鑷姩閫夋嫨鏈€浣冲帇缂╁伐鍏凤細sips 鈫?cwebp 鈫?ImageMagick 鈫?Sharp
- 鏀寔杈撳嚭鏍煎紡锛歐ebP锛堥粯璁わ級銆丳NG銆丣PEG
- 鏀寔鍗曟枃浠跺拰鐩綍鎵归噺澶勭悊
- 鍙€変繚鐣欏師鏂囦欢

## 鑴氭湰鐩綍

鑴氭湰浣嶄簬 `scripts/` 瀛愮洰褰曘€傚皢 `${SKILL_DIR}` 鏇挎崲涓?SKILL.md 鎵€鍦ㄧ洰褰曡矾寰勩€?

| 鑴氭湰 | 鐢ㄩ€?|
|------|------|
| `scripts/main.ts` | 鍥剧墖鍘嬬缉 CLI |

## 鍋忓ソ璁剧疆 (EXTEND.md)

浣跨敤 Bash 妫€鏌?EXTEND.md 瀛樺湪鎬э紙浼樺厛绾ч『搴忥級锛?

```bash
# 鍏堟鏌ラ」鐩骇
test -f .baoyu-skills/baoyu-compress-image/EXTEND.md && echo "project"

# 鍐嶆鏌ョ敤鎴风骇锛堣法骞冲彴锛?HOME 閫傜敤浜?macOS/Linux/WSL锛?
test -f "$HOME/.baoyu-skills/baoyu-compress-image/EXTEND.md" && echo "user"
```

鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                         璺緞                          鈹?     浣嶇疆         鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?.baoyu-skills/baoyu-compress-image/EXTEND.md           鈹?椤圭洰鐩綍          鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?$HOME/.baoyu-skills/baoyu-compress-image/EXTEND.md     鈹?鐢ㄦ埛涓荤洰褰?       鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?

鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?  缁撴灉    鈹?                                  鎿嶄綔                                    鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?鎵惧埌      鈹?璇诲彇銆佽В鏋愩€佸簲鐢ㄨ缃?                                                       鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?鏈壘鍒?   鈹?浣跨敤榛樿鍊?                                                                 鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?

**EXTEND.md 鏀寔椤?*锛氶粯璁ゆ牸寮?| 榛樿璐ㄩ噺 | 淇濈暀鍘熸枃浠跺亸濂?

## 鍛戒护璇硶

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts <input> [options]
```

## 鍙傛暟璇存槑

| 鍙傛暟 | 鐭弬鏁?| 璇存槑 | 榛樿鍊?|
|------|--------|------|--------|
| `<input>` | - | 杈撳叆鏂囦欢鎴栫洰褰曡矾寰?| 蹇呴渶 |
| `--output` | `-o` | 鑷畾涔夎緭鍑鸿矾寰?| 鍚岃矾寰勬柊鎵╁睍鍚?|
| `--format` | `-f` | 杈撳嚭鏍煎紡 (webp/png/jpeg) | webp |
| `--quality` | `-q` | 鍘嬬缉璐ㄩ噺 (0-100) | 80 |
| `--keep` | `-k` | 淇濈暀鍘熸枃浠?| false锛堟浛鎹級 |
| `--recursive` | `-r` | 澶勭悊瀛愮洰褰?| false |
| `--json` | - | JSON 鏍煎紡杈撳嚭缁撴灉 | false |

## 浣跨敤绀轰緥

### 鍗曟枃浠跺帇缂?

```bash
/baoyu-compress-image image.png
```

杈撳嚭锛歚image.webp`锛堟浛鎹㈠師鏂囦欢锛?

### 淇濈暀鍘熸枃浠?

```bash
/baoyu-compress-image image.png --keep
```

杈撳嚭锛歚image.webp`锛堜繚鐣?`image.png`锛?

### 鎸囧畾鏍煎紡鍜岃川閲?

```bash
/baoyu-compress-image image.png -f png -q 90
```

### 鎵归噺澶勭悊鐩綍

```bash
/baoyu-compress-image ./images/ -r -q 75
```

閫掑綊澶勭悊 `./images/` 鐩綍涓嬫墍鏈夊浘鐗囥€?

### JSON 杈撳嚭

```bash
/baoyu-compress-image image.png --json
```

杈撳嚭锛?

```json
{
  "input": "image.png",
  "output": "image.webp",
  "originalSize": 1024000,
  "compressedSize": 256000,
  "ratio": "75%"
}
```

**鏅€氳緭鍑?*锛?
```
image.png 鈫?image.webp (245KB 鈫?89KB, 64% reduction)
```

## 閰嶇疆鎵╁睍 (EXTEND.md)

鍦ㄤ互涓嬩綅缃垱寤?`EXTEND.md` 鑷畾涔夐粯璁よ缃細

- 椤圭洰绾э細`.baoyu-skills/baoyu-compress-image/EXTEND.md`
- 鐢ㄦ埛绾э細`~/.baoyu-skills/baoyu-compress-image/EXTEND.md`

```yaml
defaults:
  format: webp
  quality: 80
  keep: false
```

## 鏀寔鐨勮緭鍏ユ牸寮?

- PNG
- JPEG / JPG
- GIF
- BMP
- TIFF
- WebP

## 鍘嬬缉宸ュ叿浼樺厛绾?

1. **sips** (macOS 鍐呯疆)
2. **cwebp** (Google WebP 宸ュ叿)
3. **ImageMagick** (convert 鍛戒护)
4. **Sharp** (Node.js 搴擄紝鑷姩瀹夎)

## 渚濊禆

- Node.js 18+
- Bun锛堥€氳繃 npx 鑷姩瀹夎锛?
- 鍙€夛細cwebp銆両mageMagick锛堟彁鍗囨€ц兘锛?

## Windows 瀹夎寤鸿

```bash
# 瀹夎 ImageMagick
winget install ImageMagick.ImageMagick

# 鎴栧畨瑁?cwebp
# 浠?https://developers.google.com/speed/webp/download 涓嬭浇
```

---

## 鐗堟湰鍘嗗彶

- **v1.5.3** (2026-02-15): 涓婃父 hash 鍚屾 (8f1c4a6)
  - 鍚屾涓婃父浠撳簱鏈€鏂版彁浜?
  - 涓婃父鏂?commits 涓昏閽堝 baoyu-post-to-x 鍜?baoyu-post-to-wechat锛屼笉娑夊強鏈妧鑳?
  - 淇濈暀鏈湴瀹屾暣涓枃 SKILL.md 鍐呭

- **v1.5.2** (2026-02-12): 涓婃父 hash 鍚屾 (6cc8627)
  - 鍚屾涓婃父 v1.33.1 鍙樻洿
  - 涓婃父鏂板鎶€鑳斤紝鏈妧鑳藉唴瀹规棤鍙樺寲

- **v1.5.0** (2026-02-08): 涓婃父鍚屾 (hash 6cbf0f4)
  - 鍚屾涓婃父 scripts/main.ts 鍘嬬缉鑴氭湰
  - 鏈湴淇濈暀瀹屾暣涓枃 SKILL.md 鍐呭

- **v1.4.0** (2026-02-07): 涓婃父鍚屾
  - 鍚屾涓婃父 hash 7465f37
  - 涓婃父澶у箙绮剧畝鏂囨。锛堢Щ闄よ緟鍔╀俊鎭級锛屾湰鍦颁繚鐣欏畬鏁翠腑鏂囧唴瀹癸紙杈撳叆鏍煎紡鍒楄〃銆佸伐鍏蜂紭鍏堢骇銆乄indows 瀹夎寤鸿绛夛級
  - 鏃犳柊澧炲姛鑳芥€у彉鏇?

- **v1.2.0** (2026-02-03): 涓婃父鍚屾鍗囩骇
  - 浼樺寲杈撳嚭鏍煎紡锛堢畝娲佺洿瑙傦級
  - 鏀硅繘 JSON 杈撳嚭缁撴瀯
  - 瀹屽杽閿欒澶勭悊鍜岀姸鎬佸弽棣?

- **v1.1.0** (2026-02-02): 缁撴瀯浼樺寲
  - 娣诲姞 EXTEND.md 閰嶇疆鏀寔璇存槑
  - 浼樺寲浣跨敤璇存槑鏍煎紡锛堣〃鏍煎寲锛?
  - 缁熶竴璺緞妫€鏌ュ懡浠わ紙璺ㄥ钩鍙板吋瀹癸級

- **v1.0.0**: 鍒濆鐗堟湰
  - 鍩虹鍥剧墖鍘嬬缉鍔熻兘
  - 澶氭牸寮忔敮鎸?
  - 鎵归噺澶勭悊
