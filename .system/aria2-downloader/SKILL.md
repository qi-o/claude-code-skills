---
name: aria2-downloader
description: |
  澶氱嚎绋嬮珮閫熶笅杞藉伐鍏枫€傚綋鐢ㄦ埛闇€瑕佷笅杞芥枃浠讹紙鐗瑰埆鏄ぇ鏂囦欢锛夋垨瑙嗛鏃朵娇鐢ㄦ skill銆傝Е鍙戣瘝锛氫笅杞姐€乨ownload銆乤ria2銆佽幏鍙栨枃浠躲€佷笅杞借棰戙€乊ouTube銆丅ilibili銆丅绔欍€傝嚜鍔ㄤ娇鐢?aria2 杩涜 16 绾跨▼骞惰涓嬭浇锛屾敮鎸佹柇鐐圭画浼犮€傞泦鎴?yt-dlp 鏀寔 1000+ 瑙嗛缃戠珯涓嬭浇銆?
  Do NOT use for downloading novels/web fiction (use novel-downloader instead).
version: 3.4.0
github_url: https://github.com/yt-dlp/yt-dlp
github_hash: b8058cdf378cbbf60669b665dea146fb7dc90117
license: MIT
allowed-tools: "Bash(aria2c:*) Bash(yt-dlp:*) WebFetch"
compatibility: Requires aria2c and yt-dlp installed on system
metadata:
  category: media-tools
---

# Aria2 楂樼骇涓嬭浇鍣?

澶氬姛鑳戒笅杞藉伐鍏凤紝鏀寔 HTTP/HTTPS銆丗TP銆丅T绉嶅瓙銆佺鍔涢摼鎺ャ€佹壒閲忎笅杞姐€丟itHub Release銆?*瑙嗛涓嬭浇**绛夈€?

## 瑙﹀彂鏉′欢

褰撶敤鎴锋彁鍒颁互涓嬪唴瀹规椂浣跨敤姝?skill锛?
- "涓嬭浇"銆?download"銆?鑾峰彇鏂囦欢"
- 鎻愪緵浜嗘枃浠?URL銆佺鍔涢摼鎺ャ€佺瀛愭枃浠?
- 闇€瑕佷笅杞?GitHub Release
- 鎵归噺涓嬭浇澶氫釜鏂囦欢
- 涓嬭浇澶ф枃浠讹紙>10MB锛?
- **涓嬭浇瑙嗛**銆乊ouTube銆丅ilibili銆丅绔欍€乀witter/X 瑙嗛

## Aria2 璺緞

```
C:\Users\ZDS\AppData\Local\Microsoft\WinGet\Packages\aria2.aria2_Microsoft.Winget.Source_8wekyb3d8bbwe\aria2-1.37.0-win-64bit-build1\aria2c.exe
```

## 鍩虹鍙傛暟

```bash
aria2c -x 16 -s 16 -c --file-allocation=none "URL"
```

| 鍙傛暟 | 璇存槑 | 鎺ㄨ崘鍊?|
|------|------|--------|
| `-x` | 姣忔湇鍔″櫒鏈€澶ц繛鎺ユ暟 | 16 |
| `-s` | 鍒嗙墖鏁伴噺 | 16 |
| `-c` | 鏂偣缁紶 | 濮嬬粓鍚敤 |
| `-d` | 涓嬭浇鐩綍 | 鎸夐渶鎸囧畾 |
| `-o` | 杈撳嚭鏂囦欢鍚?| 鎸夐渶鎸囧畾 |
| `--file-allocation=none` | 蹇€熷惎鍔?| 鎺ㄨ崘 |

---

## 鍦烘櫙 1: 鏅€氭枃浠朵笅杞?

### 涓嬭浇鍒板綋鍓嶇洰褰?
```bash
aria2c -x 16 -s 16 -c "https://example.com/file.zip"
```

### 涓嬭浇鍒版寚瀹氱洰褰?
```bash
aria2c -x 16 -s 16 -c -d "C:\Users\ZDS\Downloads" "URL"
```

### 涓嬭浇骞堕噸鍛藉悕
```bash
aria2c -x 16 -s 16 -c -o "鏂版枃浠跺悕.zip" "URL"
```

---

## 鍦烘櫙 2: BT绉嶅瓙 / 纾佸姏閾炬帴涓嬭浇

### 纾佸姏閾炬帴涓嬭浇
```bash
aria2c --seed-time=0 -d "C:\Users\ZDS\Downloads" "magnet:?xt=urn:btih:HASH..."
```

### 绉嶅瓙鏂囦欢涓嬭浇
```bash
aria2c --seed-time=0 -d "C:\Users\ZDS\Downloads" "C:\path\to\file.torrent"
```

### BT 鍙傛暟璇存槑
| 鍙傛暟 | 璇存槑 |
|------|------|
| `--seed-time=0` | 涓嬭浇瀹屾垚鍚庝笉鍋氱锛堣涓?锛?|
| `--bt-stop-timeout=300` | 5鍒嗛挓鏃犻€熷害鑷姩鍋滄 |
| `--max-overall-download-limit=0` | 涓嶉檺閫?|
| `--bt-max-peers=100` | 鏈€澶ц繛鎺ヨ妭鐐规暟 |

---

## 鍦烘櫙 3: 鎵归噺涓嬭浇

### 鏂规硶1: 鍛戒护琛屽URL
```bash
aria2c -x 16 -s 16 -c "URL1" "URL2" "URL3"
```

### 鏂规硶2: 浠庢枃浠惰鍙朥RL鍒楄〃
鍏堝垱寤?`urls.txt`锛屾瘡琛屼竴涓猆RL锛?
```
https://example.com/file1.zip
https://example.com/file2.zip
https://example.com/file3.zip
```

鐒跺悗鎵ц锛?
```bash
aria2c -x 16 -s 16 -c -i urls.txt -d "C:\Users\ZDS\Downloads"
```

### 鏂规硶3: 骞惰涓嬭浇澶氫釜鏂囦欢
```bash
aria2c -x 16 -s 16 -c -j 5 -i urls.txt
```
`-j 5` 琛ㄧず鍚屾椂涓嬭浇5涓枃浠?

---

## 鍦烘櫙 4: GitHub Release 涓嬭浇

### 姝ラ1: 鑾峰彇鏈€鏂?Release 涓嬭浇閾炬帴
```bash
# 鑾峰彇浠撳簱鏈€鏂?release 鐨勮祫浜у垪琛?
curl -s "https://api.github.com/repos/OWNER/REPO/releases/latest" | grep "browser_download_url"
```

### 姝ラ2: 浣跨敤 aria2 涓嬭浇
```bash
aria2c -x 16 -s 16 -c "https://github.com/OWNER/REPO/releases/download/TAG/FILE"
```

### 甯哥敤 GitHub 涓嬭浇鍔犻€?
濡傛灉 GitHub 涓嬭浇鎱紝鍙互浣跨敤闀滃儚锛?
```bash
# 浣跨敤 ghproxy 鍔犻€?
aria2c -x 16 -s 16 -c "https://ghproxy.com/https://github.com/..."

# 鎴栦娇鐢?mirror.ghproxy.com
aria2c -x 16 -s 16 -c "https://mirror.ghproxy.com/https://github.com/..."
```

---

## 鍦烘櫙 5: 闇€瑕佽璇佺殑涓嬭浇

### 甯?Header 璁よ瘉
```bash
aria2c -x 16 -s 16 -c --header="Authorization: Bearer TOKEN" "URL"
```

### 甯?Cookie
```bash
aria2c -x 16 -s 16 -c --header="Cookie: session=xxx" "URL"
```

### HTTP 鍩烘湰璁よ瘉
```bash
aria2c -x 16 -s 16 -c --http-user=USERNAME --http-passwd=PASSWORD "URL"
```

---

## 鍦烘櫙 6: 闄愰€熶笅杞?

### 闄愬埗涓嬭浇閫熷害锛堥伩鍏嶅崰婊″甫瀹斤級
```bash
# 闄愬埗涓?5MB/s
aria2c -x 16 -s 16 -c --max-download-limit=5M "URL"
```

### 闄愬埗涓婁紶閫熷害锛圔T锛?
```bash
aria2c --seed-time=0 --max-upload-limit=100K "magnet:..."
```

---

## 鍦烘櫙 7: 浠ｇ悊涓嬭浇

### HTTP 浠ｇ悊
```bash
aria2c -x 16 -s 16 -c --all-proxy="http://127.0.0.1:7890" "URL"
```

### SOCKS5 浠ｇ悊
```bash
aria2c -x 16 -s 16 -c --all-proxy="socks5://127.0.0.1:7891" "URL"
```

---

## 鍦烘櫙 8: 鍚庡彴涓嬭浇锛堥暱鏃堕棿浠诲姟锛?

### 浣跨敤 RPC 妯″紡鍚姩 aria2 瀹堟姢杩涚▼
```bash
# 鍚姩 aria2 RPC 鏈嶅姟锛堝悗鍙拌繍琛岋級
aria2c --enable-rpc --rpc-listen-all=true --rpc-allow-origin-all -D

# 鐒跺悗閫氳繃 RPC 娣诲姞涓嬭浇浠诲姟
aria2c --rpc-secret=SECRET "URL"
```

### 绠€鍗曞悗鍙颁笅杞斤紙Windows锛?
```bash
start /B aria2c -x 16 -s 16 -c "URL" > download.log 2>&1
```

---

## 鍦烘櫙 9: 涓嬭浇鏁翠釜鐩綍/缃戠珯

### 閫掑綊涓嬭浇 FTP 鐩綍
```bash
aria2c -x 16 -s 16 -c -r "ftp://example.com/directory/"
```

---

## 鍦烘櫙 10: 瑙嗛涓嬭浇 (yt-dlp + aria2)

yt-dlp 鏀寔 **1000+ 瑙嗛缃戠珯**锛屽寘鎷?YouTube銆丅ilibili銆乀witter/X銆乂imeo銆乀ikTok 绛夈€?

> **閲嶈**: 瀹屾暣 YouTube 鏀寔闇€瑕?**yt-dlp-ejs** 鍜?JavaScript 杩愯鏃讹紙鎺ㄨ崘 Deno锛夈€?

### 鍩烘湰瑙嗛涓嬭浇
```bash
yt-dlp "VIDEO_URL"
```

### 浣跨敤 aria2 鍔犻€熶笅杞斤紙鎺ㄨ崘锛?
```bash
yt-dlp --downloader aria2c --downloader-args "aria2c:-x 16 -s 16" "VIDEO_URL"
```

### 骞跺彂鐗囨涓嬭浇锛堟柊鍔熻兘锛?
```bash
# -N 鍙傛暟鍚屾椂涓嬭浇澶氫釜鐗囨锛屽姞閫熶笅杞?
yt-dlp -N 4 "VIDEO_URL"
```

### 鎸囧畾涓嬭浇鐩綍鍜屾枃浠跺悕
```bash
yt-dlp -P "C:\Users\ZDS\Downloads" -o "%(title)s.%(ext)s" "VIDEO_URL"
```

### 閫夋嫨瑙嗛璐ㄩ噺

| 鍛戒护 | 璇存槑 |
|------|------|
| `yt-dlp -f best` | 鏈€浣宠川閲忥紙榛樿锛?|
| `yt-dlp -f "bestvideo[height<=1080]+bestaudio"` | 鏈€楂?1080p |
| `yt-dlp -f "bestvideo[height<=720]+bestaudio"` | 鏈€楂?720p |
| `yt-dlp -f "bestvideo[height<=480]+bestaudio"` | 鏈€楂?480p |

### 鍙笅杞介煶棰戯紙MP3锛?
```bash
yt-dlp -x --audio-format mp3 "VIDEO_URL"
```

### 蹇嵎棰勮锛堟柊鍔熻兘锛?
```bash
# 浣跨敤 -t 棰勮蹇€熼€夋嫨鏍煎紡
yt-dlp -t mp3 "VIDEO_URL"   # 鎻愬彇闊抽涓?MP3
yt-dlp -t aac "VIDEO_URL"   # 鎻愬彇闊抽涓?AAC
yt-dlp -t mp4 "VIDEO_URL"   # 涓嬭浇涓?MP4 (H.264/AAC)
yt-dlp -t mkv "VIDEO_URL"   # 涓嬭浇涓?MKV
```

### 娴忚鍣ㄦā鎷燂紙鏂板姛鑳斤級
```bash
# 妯℃嫙娴忚鍣ㄨ姹傜粫杩囬檺鍒讹紙闇€瑕?curl_cffi锛?
yt-dlp --impersonate chrome "VIDEO_URL"
yt-dlp --impersonate safari:macos "VIDEO_URL"
```

### SponsorBlock 闆嗘垚锛堟柊鍔熻兘锛?
```bash
# 鑷姩绉婚櫎 YouTube 瑙嗛涓殑璧炲姪鐗囨
yt-dlp --sponsorblock-remove sponsor "VIDEO_URL"

# 鏍囪璧炲姪鐗囨涓虹珷鑺?
yt-dlp --sponsorblock-mark sponsor "VIDEO_URL"
```

### 绔犺妭鍒嗗壊锛堟柊鍔熻兘锛?
```bash
# 鎸夌珷鑺傚垎鍓茶棰戜负澶氫釜鏂囦欢
yt-dlp --split-chapters "VIDEO_URL"
```

### 涓嬭浇鎾斁鍒楄〃
```bash
# 涓嬭浇鏁翠釜鎾斁鍒楄〃
yt-dlp "PLAYLIST_URL"

# 鍙笅杞芥挱鏀惧垪琛ㄤ腑鐨勭 1-5 涓棰?
yt-dlp --playlist-items 1-5 "PLAYLIST_URL"
```

### 涓嬭浇瀛楀箷
```bash
# 涓嬭浇瑙嗛鍜屽瓧骞?
yt-dlp --write-subs --sub-langs "zh-Hans,en" "VIDEO_URL"

# 鍙笅杞藉瓧骞曪紙涓嶄笅杞借棰戯級
yt-dlp --skip-download --write-subs "VIDEO_URL"
```

### 甯哥敤骞冲彴绀轰緥

**YouTube**
```bash
yt-dlp --downloader aria2c "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Bilibili (B绔?**
```bash
yt-dlp --downloader aria2c "https://www.bilibili.com/video/BV..."
```

**Twitter/X**
```bash
yt-dlp "https://twitter.com/user/status/..."
```

### yt-dlp 甯哥敤鍙傛暟

| 鍙傛暟 | 璇存槑 |
|------|------|
| `-P PATH` | 涓嬭浇鐩綍 |
| `-o TEMPLATE` | 杈撳嚭鏂囦欢鍚嶆ā鏉?|
| `-f FORMAT` | 瑙嗛鏍煎紡/璐ㄩ噺 |
| `-x` | 鍙彁鍙栭煶棰?|
| `--audio-format mp3` | 闊抽鏍煎紡 |
| `-t PRESET` | 蹇嵎棰勮 (mp3/aac/mp4/mkv) |
| `-N NUM` | 骞跺彂鐗囨涓嬭浇鏁?|
| `--impersonate CLIENT` | 娴忚鍣ㄦā鎷?|
| `--sponsorblock-remove` | 绉婚櫎璧炲姪鐗囨 |
| `--split-chapters` | 鎸夌珷鑺傚垎鍓?|
| `--write-subs` | 涓嬭浇瀛楀箷 |
| `--sub-langs LANGS` | 瀛楀箷璇█ |
| `--downloader aria2c` | 浣跨敤 aria2 涓嬭浇 |
| `--cookies-from-browser chrome` | 浣跨敤娴忚鍣?cookies锛堥渶瑕佺櫥褰曠殑瑙嗛锛?|
| `--list-formats` | 鍒楀嚭鍙敤鏍煎紡 |
| `--update-to CHANNEL` | 鍒囨崲鍙戝竷娓犻亾 (stable/nightly/master) |
| `--compat-options 2025` | 鍏煎 2025 骞磋涓?|
| `--format-sort-reset` | 閲嶇疆鏍煎紡鎺掑簭 |

---

## 甯哥敤鐩綍蹇嵎鏂瑰紡

| 浣嶇疆 | 璺緞 |
|------|------|
| 妗岄潰 | `C:\Users\ZDS\Desktop` |
| 涓嬭浇 | `C:\Users\ZDS\Downloads` |
| 鏂囨。 | `C:\Users\ZDS\Documents` |

---

## 鏁呴殰鎺掗櫎

### 涓嬭浇澶辫触/閫熷害鎱?
1. 闄嶄綆杩炴帴鏁帮細`-x 8 -s 8`
2. 娣诲姞 User-Agent锛歚--user-agent="Mozilla/5.0..."`
3. 浣跨敤浠ｇ悊

### 鏈嶅姟鍣ㄤ笉鏀寔澶氱嚎绋?
```bash
aria2c -x 1 -s 1 -c "URL"
```

### 璇佷功閿欒
```bash
aria2c --check-certificate=false "URL"
```

---

## 蹇€熷弬鑰冨崱鐗?

```
# 鏅€氫笅杞?
aria2c -x 16 -s 16 -c "URL"

# 纾佸姏閾炬帴
aria2c --seed-time=0 "magnet:?xt=..."

# 鎵归噺涓嬭浇
aria2c -x 16 -s 16 -c -j 5 -i urls.txt

# GitHub 鍔犻€?
aria2c -x 16 -s 16 -c "https://ghproxy.com/GITHUB_URL"

# 甯︿唬鐞?
aria2c --all-proxy="http://127.0.0.1:7890" "URL"

# 瑙嗛涓嬭浇锛坅ria2 鍔犻€燂級
yt-dlp --downloader aria2c --downloader-args "aria2c:-x 16 -s 16" "VIDEO_URL"

# 骞跺彂鐗囨涓嬭浇
yt-dlp -N 4 "VIDEO_URL"

# 蹇嵎棰勮涓嬭浇
yt-dlp -t mp3 "VIDEO_URL"
yt-dlp -t mp4 "VIDEO_URL"

# 鍙笅杞介煶棰?
yt-dlp -x --audio-format mp3 "VIDEO_URL"

# 娴忚鍣ㄦā鎷燂紙缁曡繃闄愬埗锛?
yt-dlp --impersonate chrome "VIDEO_URL"

# 绉婚櫎璧炲姪鐗囨
yt-dlp --sponsorblock-remove sponsor "VIDEO_URL"

# B绔欒棰?
yt-dlp --downloader aria2c "https://www.bilibili.com/video/BV..."

# 鏇存柊 yt-dlp 鍒?nightly 鐗堟湰
yt-dlp --update-to nightly
```

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 下载完成后自动通知用户
- BT/磁力下载时默认添加 --seed-time=0 参数
- 视频下载时优先使用 aria2 作为外部下载器加速
- 更新 skill 时需要完整对比上游 README 的功能变化，不能只更新 hash
- aria2-downloader skill 更新时采用混合策略，保留中文化场景教程
- 更新 aria2-downloader skill 时应同步检查 yt-dlp 程序版本
- 如果 yt-dlp 有新版本应运行 yt-dlp -U 更新
- 更新 aria2-downloader skill 后应检查 yt-dlp 程序版本

### Known Fixes & Workarounds
- Windows 下 aria2c 可能不在 PATH 中，需使用完整路径
- BT 下载使用 --seed-time=0 可在下载完成后立即停止做种
- 长时间下载任务应使用后台模式运行，通过 TaskOutput 检查进度
- yt-dlp 下载 B站视频时可能需要 --cookies-from-browser 参数获取高清画质
- 通过 github_url 和 github_hash 字段追踪 yt-dlp 更新，当 skill-manager 显示 outdated 时运行 yt-dlp -U 更新
- yt-dlp 路径: C:/Users/ZDS/AppData/Local/Microsoft/WinGet/Packages/yt-dlp.yt-dlp_Microsoft.Winget.Source_8wekyb3d8bbwe/yt-dlp.exe
- ffmpeg 路径: C:/Users/ZDS/AppData/Local/Microsoft/WinGet/Packages/yt-dlp.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-N-122319-gf6a95c7eb7-win64-gpl/bin/ffmpeg.exe
- yt-dlp 下载 B站视频时会分别下载视频和音频，需要 ffmpeg 合并
- yt-dlp 完整 YouTube 支持需要 yt-dlp-ejs 和 JavaScript 运行时（推荐 Deno）
- yt-dlp 新增 -t 预设别名（mp3/aac/mp4/mkv）快速选择格式
- yt-dlp 新增 --impersonate 浏览器模拟功能需要 curl_cffi
- yt-dlp 新增 --sponsorblock-remove 移除 YouTube 赞助片段
- yt-dlp 新增 -N 参数并发片段下载
- yt-dlp 上游更新通常只是新增网站支持，无需同步修改文档内容
- skill版本号采用minor递增表示上游功能同步(如3.2.0→3.2.1)
- yt-dlp 通过 pip 安装时，不能用 yt-dlp -U 更新，需用 pip install --upgrade yt-dlp
- WinGet 安装的 yt-dlp 可能因证书问题更新失败，pip 是更可靠的更新方式

### Custom Instruction Injection

更新 aria2-downloader skill 后主动提示检查 yt-dlp 版本