---
name: aria2-downloader
description: |
  多线程高速下载工具。当用户需要下载文件（特别是大文件）或视频时使用此 skill。触发词：下载、download、aria2、获取文件、下载视频、YouTube、Bilibili、B站。自动使用 aria2 进行 16 线程并行下载，支持断点续传。集成 yt-dlp 支持 1000+ 视频网站下载。
  Do NOT use for downloading novels/web fiction (use novel-downloader instead).
version: 3.3.4
github_url: https://github.com/yt-dlp/yt-dlp
github_hash: 35684c1171dd8b99da825cf43a0b2c06b43824b7
license: MIT
allowed-tools: "Bash(aria2c:*) Bash(yt-dlp:*) WebFetch"
compatibility: Requires aria2c and yt-dlp installed on system
metadata:
  category: media-tools
---

# Aria2 高级下载器

多功能下载工具，支持 HTTP/HTTPS、FTP、BT种子、磁力链接、批量下载、GitHub Release、**视频下载**等。

## 触发条件

当用户提到以下内容时使用此 skill：
- "下载"、"download"、"获取文件"
- 提供了文件 URL、磁力链接、种子文件
- 需要下载 GitHub Release
- 批量下载多个文件
- 下载大文件（>10MB）
- **下载视频**、YouTube、Bilibili、B站、Twitter/X 视频

## Aria2 路径

```
C:\Users\ZDS\AppData\Local\Microsoft\WinGet\Packages\aria2.aria2_Microsoft.Winget.Source_8wekyb3d8bbwe\aria2-1.37.0-win-64bit-build1\aria2c.exe
```

## 基础参数

```bash
aria2c -x 16 -s 16 -c --file-allocation=none "URL"
```

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `-x` | 每服务器最大连接数 | 16 |
| `-s` | 分片数量 | 16 |
| `-c` | 断点续传 | 始终启用 |
| `-d` | 下载目录 | 按需指定 |
| `-o` | 输出文件名 | 按需指定 |
| `--file-allocation=none` | 快速启动 | 推荐 |

---

## 场景 1: 普通文件下载

### 下载到当前目录
```bash
aria2c -x 16 -s 16 -c "https://example.com/file.zip"
```

### 下载到指定目录
```bash
aria2c -x 16 -s 16 -c -d "C:\Users\ZDS\Downloads" "URL"
```

### 下载并重命名
```bash
aria2c -x 16 -s 16 -c -o "新文件名.zip" "URL"
```

---

## 场景 2: BT种子 / 磁力链接下载

### 磁力链接下载
```bash
aria2c --seed-time=0 -d "C:\Users\ZDS\Downloads" "magnet:?xt=urn:btih:HASH..."
```

### 种子文件下载
```bash
aria2c --seed-time=0 -d "C:\Users\ZDS\Downloads" "C:\path\to\file.torrent"
```

### BT 参数说明
| 参数 | 说明 |
|------|------|
| `--seed-time=0` | 下载完成后不做种（设为0） |
| `--bt-stop-timeout=300` | 5分钟无速度自动停止 |
| `--max-overall-download-limit=0` | 不限速 |
| `--bt-max-peers=100` | 最大连接节点数 |

---

## 场景 3: 批量下载

### 方法1: 命令行多URL
```bash
aria2c -x 16 -s 16 -c "URL1" "URL2" "URL3"
```

### 方法2: 从文件读取URL列表
先创建 `urls.txt`，每行一个URL：
```
https://example.com/file1.zip
https://example.com/file2.zip
https://example.com/file3.zip
```

然后执行：
```bash
aria2c -x 16 -s 16 -c -i urls.txt -d "C:\Users\ZDS\Downloads"
```

### 方法3: 并行下载多个文件
```bash
aria2c -x 16 -s 16 -c -j 5 -i urls.txt
```
`-j 5` 表示同时下载5个文件

---

## 场景 4: GitHub Release 下载

### 步骤1: 获取最新 Release 下载链接
```bash
# 获取仓库最新 release 的资产列表
curl -s "https://api.github.com/repos/OWNER/REPO/releases/latest" | grep "browser_download_url"
```

### 步骤2: 使用 aria2 下载
```bash
aria2c -x 16 -s 16 -c "https://github.com/OWNER/REPO/releases/download/TAG/FILE"
```

### 常用 GitHub 下载加速
如果 GitHub 下载慢，可以使用镜像：
```bash
# 使用 ghproxy 加速
aria2c -x 16 -s 16 -c "https://ghproxy.com/https://github.com/..."

# 或使用 mirror.ghproxy.com
aria2c -x 16 -s 16 -c "https://mirror.ghproxy.com/https://github.com/..."
```

---

## 场景 5: 需要认证的下载

### 带 Header 认证
```bash
aria2c -x 16 -s 16 -c --header="Authorization: Bearer TOKEN" "URL"
```

### 带 Cookie
```bash
aria2c -x 16 -s 16 -c --header="Cookie: session=xxx" "URL"
```

### HTTP 基本认证
```bash
aria2c -x 16 -s 16 -c --http-user=USERNAME --http-passwd=PASSWORD "URL"
```

---

## 场景 6: 限速下载

### 限制下载速度（避免占满带宽）
```bash
# 限制为 5MB/s
aria2c -x 16 -s 16 -c --max-download-limit=5M "URL"
```

### 限制上传速度（BT）
```bash
aria2c --seed-time=0 --max-upload-limit=100K "magnet:..."
```

---

## 场景 7: 代理下载

### HTTP 代理
```bash
aria2c -x 16 -s 16 -c --all-proxy="http://127.0.0.1:7890" "URL"
```

### SOCKS5 代理
```bash
aria2c -x 16 -s 16 -c --all-proxy="socks5://127.0.0.1:7891" "URL"
```

---

## 场景 8: 后台下载（长时间任务）

### 使用 RPC 模式启动 aria2 守护进程
```bash
# 启动 aria2 RPC 服务（后台运行）
aria2c --enable-rpc --rpc-listen-all=true --rpc-allow-origin-all -D

# 然后通过 RPC 添加下载任务
aria2c --rpc-secret=SECRET "URL"
```

### 简单后台下载（Windows）
```bash
start /B aria2c -x 16 -s 16 -c "URL" > download.log 2>&1
```

---

## 场景 9: 下载整个目录/网站

### 递归下载 FTP 目录
```bash
aria2c -x 16 -s 16 -c -r "ftp://example.com/directory/"
```

---

## 场景 10: 视频下载 (yt-dlp + aria2)

yt-dlp 支持 **1000+ 视频网站**，包括 YouTube、Bilibili、Twitter/X、Vimeo、TikTok 等。

> **重要**: 完整 YouTube 支持需要 **yt-dlp-ejs** 和 JavaScript 运行时（推荐 Deno）。

### 基本视频下载
```bash
yt-dlp "VIDEO_URL"
```

### 使用 aria2 加速下载（推荐）
```bash
yt-dlp --downloader aria2c --downloader-args "aria2c:-x 16 -s 16" "VIDEO_URL"
```

### 并发片段下载（新功能）
```bash
# -N 参数同时下载多个片段，加速下载
yt-dlp -N 4 "VIDEO_URL"
```

### 指定下载目录和文件名
```bash
yt-dlp -P "C:\Users\ZDS\Downloads" -o "%(title)s.%(ext)s" "VIDEO_URL"
```

### 选择视频质量

| 命令 | 说明 |
|------|------|
| `yt-dlp -f best` | 最佳质量（默认） |
| `yt-dlp -f "bestvideo[height<=1080]+bestaudio"` | 最高 1080p |
| `yt-dlp -f "bestvideo[height<=720]+bestaudio"` | 最高 720p |
| `yt-dlp -f "bestvideo[height<=480]+bestaudio"` | 最高 480p |

### 只下载音频（MP3）
```bash
yt-dlp -x --audio-format mp3 "VIDEO_URL"
```

### 快捷预设（新功能）
```bash
# 使用 -t 预设快速选择格式
yt-dlp -t mp3 "VIDEO_URL"   # 提取音频为 MP3
yt-dlp -t aac "VIDEO_URL"   # 提取音频为 AAC
yt-dlp -t mp4 "VIDEO_URL"   # 下载为 MP4 (H.264/AAC)
yt-dlp -t mkv "VIDEO_URL"   # 下载为 MKV
yt-dlp -t sleep "VIDEO_URL" # 下载为休眠/屏保视频
```

### 浏览器模拟（新功能）
```bash
# 模拟浏览器请求绕过限制（需要 curl_cffi）
yt-dlp --impersonate chrome "VIDEO_URL"
yt-dlp --impersonate safari:macos "VIDEO_URL"
```

### SponsorBlock 集成（新功能）
```bash
# 自动移除 YouTube 视频中的赞助片段
yt-dlp --sponsorblock-remove sponsor "VIDEO_URL"

# 标记赞助片段为章节
yt-dlp --sponsorblock-mark sponsor "VIDEO_URL"
```

### 章节分割（新功能）
```bash
# 按章节分割视频为多个文件
yt-dlp --split-chapters "VIDEO_URL"
```

### 下载播放列表
```bash
# 下载整个播放列表
yt-dlp "PLAYLIST_URL"

# 只下载播放列表中的第 1-5 个视频
yt-dlp --playlist-items 1-5 "PLAYLIST_URL"
```

### 直播流下载
```bash
# 从当前时间开始下载直播流（不从开头下载）
yt-dlp --no-live-from-start "LIVE_URL"

# 等待直播开始（最多等待 60 分钟）
yt-dlp --wait-for-video 60 "LIVE_URL"
```

### 下载字幕
```bash
# 下载视频和字幕
yt-dlp --write-subs --sub-langs "zh-Hans,en" "VIDEO_URL"

# 只下载字幕（不下载视频）
yt-dlp --skip-download --write-subs "VIDEO_URL"
```

### 常用平台示例

**YouTube**
```bash
yt-dlp --downloader aria2c "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Bilibili (B站)**
```bash
yt-dlp --downloader aria2c "https://www.bilibili.com/video/BV..."
```

**Twitter/X**
```bash
yt-dlp "https://twitter.com/user/status/..."
```

### yt-dlp 常用参数

| 参数 | 说明 |
|------|------|
| `-P PATH` | 下载目录 |
| `-o TEMPLATE` | 输出文件名模板 |
| `-f FORMAT` | 视频格式/质量 |
| `-x` | 只提取音频 |
| `--audio-format mp3` | 音频格式 |
| `-t PRESET` | 快捷预设 (mp3/aac/mp4/mkv) |
| `-N NUM` | 并发片段下载数 |
| `--impersonate CLIENT` | 浏览器模拟 |
| `--sponsorblock-remove` | 移除赞助片段 |
| `--split-chapters` | 按章节分割 |
| `--write-subs` | 下载字幕 |
| `--sub-langs LANGS` | 字幕语言 |
| `--downloader aria2c` | 使用 aria2 下载 |
| `--cookies-from-browser chrome` | 使用浏览器 cookies（需要登录的视频） |
| `--list-formats` | 列出可用格式 |
| `--update-to CHANNEL` | 切换发布渠道 (stable/nightly/master) |
| `--compat-options 2025` | 兼容 2025 年行为 |
| `--format-sort-reset` | 重置格式排序 |
| `--wait-for-video MIN` | 等待直播流开始（分钟） |
| `--no-live-from-start` | 从当前时间下载直播流 |
| `--alias ALIAS ARGS` | 创建自定义命令别名 |

---

## 常用目录快捷方式

| 位置 | 路径 |
|------|------|
| 桌面 | `C:\Users\ZDS\Desktop` |
| 下载 | `C:\Users\ZDS\Downloads` |
| 文档 | `C:\Users\ZDS\Documents` |

---

## 故障排除

### 下载失败/速度慢
1. 降低连接数：`-x 8 -s 8`
2. 添加 User-Agent：`--user-agent="Mozilla/5.0..."`
3. 使用代理

### 服务器不支持多线程
```bash
aria2c -x 1 -s 1 -c "URL"
```

### 证书错误
```bash
aria2c --check-certificate=false "URL"
```

---

## 快速参考卡片

```
# 普通下载
aria2c -x 16 -s 16 -c "URL"

# 磁力链接
aria2c --seed-time=0 "magnet:?xt=..."

# 批量下载
aria2c -x 16 -s 16 -c -j 5 -i urls.txt

# GitHub 加速
aria2c -x 16 -s 16 -c "https://ghproxy.com/GITHUB_URL"

# 带代理
aria2c --all-proxy="http://127.0.0.1:7890" "URL"

# 视频下载（aria2 加速）
yt-dlp --downloader aria2c --downloader-args "aria2c:-x 16 -s 16" "VIDEO_URL"

# 并发片段下载
yt-dlp -N 4 "VIDEO_URL"

# 快捷预设下载
yt-dlp -t mp3 "VIDEO_URL"
yt-dlp -t mp4 "VIDEO_URL"
yt-dlp -t sleep "VIDEO_URL"

# 只下载音频
yt-dlp -x --audio-format mp3 "VIDEO_URL"

# 浏览器模拟（绕过限制）
yt-dlp --impersonate chrome "VIDEO_URL"

# 移除赞助片段
yt-dlp --sponsorblock-remove sponsor "VIDEO_URL"

# B站视频
yt-dlp --downloader aria2c "https://www.bilibili.com/video/BV..."

# 更新 yt-dlp 到 nightly 版本
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
- yt-dlp 新增 -t sleep 预设、--wait-for-video 等待直播、--no-live-from-start 从当前时间下载直播流、--alias 自定义命令别名
- aria2-downloader 版本号从 3.3.0 升至 3.3.1，新增直播流下载场景和参数表条目

### Custom Instruction Injection

更新 aria2-downloader skill 后主动提示检查 yt-dlp 版本

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 大文件下载 (>1GB) | URL 指向大文件或磁力链接 | 确认磁盘空间和下载目录 |
| 批量下载 | 使用 -i urls.txt 或多个 URL | 确认文件列表和总大小，避免意外消耗带宽 |
| 视频下载需要 cookies | 视频平台提示登录才能下载高清 | 确认是否使用 --cookies-from-browser 导出浏览器 cookies |
| BT/磁力下载 | 用户提供了磁力链接或种子 | 确认 --seed-time=0（不做种）和下载目录 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| 下载速度为 0 或失败 | aria2c 退出码非 0 | 降低连接数 (-x 8 -s 8)，添加 --user-agent，或使用代理 |
| 证书验证失败 | SSL 错误日志 | 添加 --check-certificate=false 临时绕过 |
| yt-dlp 提取失败 | 视频平台更新导致下载失败 | 运行 `yt-dlp -U` 更新到最新版；回退到浏览器模拟 `--impersonate chrome` |
| 磁力链接无节点 | BT 下载长时间无速度 | 提示用户检查磁力链接有效性，或添加 tracker 列表 |
| 磁盘空间不足 | 下载中途报错 | 提示用户清理磁盘，或使用 -d 指向有空间的目录 |