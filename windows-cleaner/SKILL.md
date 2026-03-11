---
name: windows-cleaner
description: Analyze and reclaim Windows disk space through intelligent cleanup recommendations. Use when users report disk space issues, need to clean up their Windows PC, or want to understand what's consuming storage. Use when user says "清理磁盘", "磁盘空间", "disk cleanup", "C盘满浜?, "释放空间", or "storage analysis".
license: MIT
allowed-tools: "Bash(powershell:*) Read"
version: 0.1.0
metadata:
  category: domain-specific
---

# Windows Cleaner

## Overview

分析 Windows 磁盘ʹ用情况，提供安鍏ㄧ殑娓呯悊寤鸿。遵寰?*安ȫ优先**ԭ则：先分析，再纭，最后ִ琛屻€?

## 核心ԭ则

1. **安ȫ绗竴**：ɾ闄ゆ搷浣滃繀椤荤敤鎴风‘璁?
2. **浠峰€间紭鍏?*：不Ϊ了数字好看而ɾ闄ゆ湁鐢ㄧ殑缂撳瓨
3. **网络鐜意ʶ**锛氳€冭檻閲嶆柊涓嬭浇鐨勬椂闂存垚鏈?
4. **Ӱ响分析**：ÿ涓竻鐞嗗缓璁繀椤昏明ɾ闄ゅ悗鏋?

## 鎶€鏈点：PowerShell 鎵ц方ʽ

**关键**锛氬鏉?PowerShell 命令必须д成 `.ps1` 脚本文件鎵ц，不能内联ִ琛屻€?

### 正ȷ方ʽ

```bash
# 1. ʹ用 Write 宸ュ叿鍐欏叆鑴氭湰鏂囦欢
# Write tool -> C:\Users\USERNAME\script.ps1

# 2. 鎵ц脚本
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\USERNAME\script.ps1"

# 3. ɾ除脚本
rm -f "C:\Users\USERNAME\script.ps1"
```

### 閿欒方ʽ（会因ת义问棰樺け璐ワ級

```bash
# 这Щ浼氬け璐ワ細
powershell -Command "Get-PSDrive | Select-Object @{N='Size';E={$_.Used}}"  # ʧ败
powershell -Command "$arr = @('a','b'); foreach ($i in $arr) { ... }"      # ʧ败
powershell -Command "... $_.Property ..."                                   # ʧ败
```

### 绠€单命浠ゅ彲浠ュ唴鑱?

```bash
# 这Щ绠€单命浠ゅ彲浠ュ唴鑱旓細
powershell -NoProfile -Command "(Get-PSDrive C).Free / 1GB"
powershell -NoProfile -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
powershell -NoProfile -Command "Test-Path 'C:\some\path'"
powershell -NoProfile -Command "Remove-Item -Path 'C:\path' -Recurse -Force"
```

## 分析脚本妯℃澘

### 脚本 1锛氱鐩樻瑙?(disk_overview.ps1)

```powershell
Write-Host "=== Disk Space Overview ===" -ForegroundColor Cyan

Get-PSDrive -PSProvider FileSystem | ForEach-Object {
    $usedGB = [math]::Round($_.Used/1GB, 2)
    $freeGB = [math]::Round($_.Free/1GB, 2)
    $totalGB = [math]::Round(($_.Used + $_.Free)/1GB, 2)
    $usedPercent = if ($totalGB -gt 0) { [math]::Round(($usedGB / $totalGB) * 100, 1) } else { 0 }
    Write-Host "$($_.Name): Used: $usedGB GB | Free: $freeGB GB | Total: $totalGB GB | Usage: $usedPercent%"
}
```

### 脚本 2：用户文浠跺す分析 (user_folders.ps1)

```powershell
Write-Host "=== User Temp Folder ===" -ForegroundColor Yellow
$tempPath = $env:TEMP
if (Test-Path $tempPath) {
    $tempSize = (Get-ChildItem -Path $tempPath -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Write-Host "User Temp: $([math]::Round($tempSize/1GB, 2)) GB"
}

Write-Host "`n=== Downloads Folder ===" -ForegroundColor Yellow
# 閲嶈：ʹ鐢?$env:USERPROFILE\Downloads，不Ҫ用 [Environment]::GetFolderPath("Downloads")
$downloadsPath = "$env:USERPROFILE\Downloads"
if (Test-Path $downloadsPath) {
    $totalSize = (Get-ChildItem -Path $downloadsPath -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Write-Host "Downloads total: $([math]::Round($totalSize/1GB, 2)) GB"

    Write-Host "`nLarge files (>50MB):"
    Get-ChildItem -Path $downloadsPath -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Length -gt 50MB } |
        Sort-Object Length -Descending |
        Select-Object -First 10 |
        ForEach-Object {
            Write-Host "  $([math]::Round($_.Length/1MB, 0)) MB - $($_.Name)"
        }
}

Write-Host "`n=== Recycle Bin ===" -ForegroundColor Yellow
try {
    $shell = New-Object -ComObject Shell.Application
    $recycleBin = $shell.NameSpace(0x0a)
    $items = $recycleBin.Items()
    Write-Host "Items in Recycle Bin: $($items.Count)"
} catch {
    Write-Host "Could not access Recycle Bin"
}
```

### 脚本 3：AppData 澶ф枃浠跺す分析 (appdata_analysis.ps1)

```powershell
Write-Host "=== AppData\Local Large Folders ===" -ForegroundColor Yellow
Get-ChildItem -Path $env:LOCALAPPDATA -Directory -Force -ErrorAction SilentlyContinue |
    ForEach-Object {
        $size = (Get-ChildItem -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                 Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($size/1GB, 2)}
    } | Where-Object { $_.SizeGB -gt 0.1 } |
    Sort-Object SizeGB -Descending |
    Select-Object -First 20 |
    ForEach-Object { Write-Host "$($_.SizeGB) GB - $($_.Name)" }

Write-Host "`n=== AppData\Roaming Large Folders ===" -ForegroundColor Yellow
Get-ChildItem -Path $env:APPDATA -Directory -Force -ErrorAction SilentlyContinue |
    ForEach-Object {
        $size = (Get-ChildItem -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                 Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($size/1GB, 2)}
    } | Where-Object { $_.SizeGB -gt 0.1 } |
    Sort-Object SizeGB -Descending |
    Select-Object -First 20 |
    ForEach-Object { Write-Host "$($_.SizeGB) GB - $($_.Name)" }

Write-Host "`n=== Hidden Folders in User Profile ===" -ForegroundColor Yellow
Get-ChildItem -Path $env:USERPROFILE -Directory -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like ".*" } |
    ForEach-Object {
        $size = (Get-ChildItem -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                 Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($size/1GB, 2)}
    } | Where-Object { $_.SizeGB -gt 0.05 } |
    Sort-Object SizeGB -Descending |
    ForEach-Object { Write-Host "$($_.SizeGB) GB - $($_.Name)" }
```

### 脚本 4：开鍙戣€呯紦瀛樺垎鏋?(dev_caches.ps1)

```powershell
Write-Host "=== Developer Caches ===" -ForegroundColor Cyan

# 定义瑕佹鏌ョ殑缂撳瓨璺緞锛堟瘡涓紦瀛樺彲鑳芥湁澶氫釜浣嶇疆锛?
$caches = @{
    "npm cache" = @("$env:LOCALAPPDATA\npm-cache", "$env:APPDATA\npm-cache")
    "pip cache" = @("$env:LOCALAPPDATA\pip\cache")
    "uv cache" = @("$env:LOCALAPPDATA\uv")
    "pnpm store" = @("$env:LOCALAPPDATA\pnpm\store", "$env:LOCALAPPDATA\pnpm-store")
    "NuGet packages" = @("$env:USERPROFILE\.nuget\packages")
    "Cargo cache" = @("$env:USERPROFILE\.cargo")
    "Go modules" = @("$env:USERPROFILE\go\pkg\mod")
    "Bun cache" = @("$env:USERPROFILE\.bun")
    "Rustup" = @("$env:USERPROFILE\.rustup")
}

foreach ($cache in $caches.GetEnumerator()) {
    foreach ($path in $cache.Value) {
        if (Test-Path $path) {
            $size = (Get-ChildItem -Path $path -Recurse -Force -ErrorAction SilentlyContinue |
                     Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
            Write-Host "$($cache.Key): $([math]::Round($size/1GB, 2)) GB ($path)"
            break
        }
    }
}

# Conda/Miniconda
$condaPaths = @("$env:USERPROFILE\miniconda3", "$env:USERPROFILE\Miniconda3", "$env:USERPROFILE\anaconda3", "$env:USERPROFILE\Anaconda3")
foreach ($path in $condaPaths) {
    if (Test-Path $path) {
        $size = (Get-ChildItem -Path $path -Recurse -Force -ErrorAction SilentlyContinue |
                 Measure-Object -Property Length -Sum).Sum
        Write-Host "Conda: $([math]::Round($size/1GB, 2)) GB ($path)"
        break
    }
}

# Playwright browsers
Write-Host "`n=== Playwright Browsers ===" -ForegroundColor Yellow
$playwrightPath = "$env:LOCALAPPDATA\ms-playwright"
if (Test-Path $playwrightPath) {
    Get-ChildItem -Path $playwrightPath -Directory -Force -ErrorAction SilentlyContinue |
        ForEach-Object {
            $size = (Get-ChildItem -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                     Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
            if ($size -gt 10MB) {
                Write-Host "  $([math]::Round($size/1MB, 0)) MB - $($_.Name)"
            }
        }
} else {
    Write-Host "Playwright not found"
}

# .cache folder
Write-Host "`n=== .cache Folder ===" -ForegroundColor Yellow
$cachePath = "$env:USERPROFILE\.cache"
if (Test-Path $cachePath) {
    Get-ChildItem -Path $cachePath -Directory -Force -ErrorAction SilentlyContinue |
        ForEach-Object {
            $size = (Get-ChildItem -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                     Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
            if ($size -gt 50MB) {
                Write-Host "  $([math]::Round($size/1GB, 2)) GB - $($_.Name)"
            }
        }
} else {
    Write-Host ".cache folder not found"
}

# Docker
Write-Host "`n=== Docker ===" -ForegroundColor Yellow
if (Get-Command docker -ErrorAction SilentlyContinue) {
    try {
        docker system df 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Docker not running"
        }
    } catch {
        Write-Host "Docker not accessible"
    }
} else {
    Write-Host "Docker not installed"
}
```

## 清理脚本妯℃澘

### 清理 Playwright 鏃х増鏈?(cleanup_playwright.ps1)

```powershell
$basePath = "$env:LOCALAPPDATA\ms-playwright"
if (-not (Test-Path $basePath)) {
    Write-Host "Playwright not found"
    exit
}

$browsers = @("chromium", "chromium_headless_shell", "firefox", "webkit")
$totalCleaned = 0

foreach ($browser in $browsers) {
    $versions = Get-ChildItem -Path $basePath -Directory -Filter "$browser-*" -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending

    if ($versions.Count -gt 1) {
        $toDelete = $versions | Select-Object -Skip 1
        foreach ($ver in $toDelete) {
            $size = (Get-ChildItem -Path $ver.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                     Measure-Object -Property Length -Sum).Sum
            Remove-Item -Path $ver.FullName -Recurse -Force -ErrorAction SilentlyContinue
            $totalCleaned += $size
            Write-Host "Removed: $($ver.Name) ($([math]::Round($size/1MB, 0)) MB)"
        }
    }
}

Write-Host "`nTotal cleaned: $([math]::Round($totalCleaned/1GB, 2)) GB"
```

### 清理 npm _npx 缓存 (cleanup_npx.ps1)

```powershell
$paths = @("$env:LOCALAPPDATA\npm-cache\_npx", "$env:APPDATA\npm-cache\_npx")
$cleaned = $false

foreach ($npxPath in $paths) {
    if (Test-Path $npxPath) {
        $size = (Get-ChildItem -Path $npxPath -Recurse -Force -ErrorAction SilentlyContinue |
                 Measure-Object -Property Length -Sum).Sum
        Remove-Item -Path $npxPath -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "Cleaned npm _npx: $([math]::Round($size/1MB, 0)) MB from $npxPath"
        $cleaned = $true
    }
}

if (-not $cleaned) {
    Write-Host "npm _npx cache not found"
}
```

### 清理 puppeteer 缓存 (cleanup_puppeteer.ps1)

```powershell
$puppeteerPath = "$env:USERPROFILE\.cache\puppeteer"
if (Test-Path $puppeteerPath) {
    $size = (Get-ChildItem -Path $puppeteerPath -Recurse -Force -ErrorAction SilentlyContinue |
             Measure-Object -Property Length -Sum).Sum
    Remove-Item -Path $puppeteerPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Cleaned puppeteer cache: $([math]::Round($size/1GB, 2)) GB"
} else {
    Write-Host "Puppeteer cache not found"
}
```

## 清理分类琛?

### [SAFE] 安ȫ清理项Ŀ

| 项Ŀ | Ӱ响 | 清理方ʽ |
|------|------|----------|
| 回收绔?| 鏃?| `Clear-RecycleBin -Force` |
| 鏃х増 Playwright 娴忚鍣?| 无（保留鏈€新版鏈級 | cleanup_playwright.ps1 |
| npm _npx 缓存 | npx 涓嬫ʹ用ʱ重新下杞?| cleanup_npx.ps1 |
| puppeteer 缓存 | 闇€Ҫʱ重新下载 | cleanup_puppeteer.ps1 |
| 超过7澶╃殑 Temp 文件 | 鏃?| 脚本鎴?cleanmgr |
| Windows Update 缓存 | 无（闇€管理ԱȨ限） | cleanmgr |

### [TRADEOFF] 闇€纭的清理项鐩?

| 项Ŀ | Ӱ响 | 备ע |
|------|------|------|
| npm _cacache | npm install 闇€重新下载 | 国内网络较慢 |
| pip cache | pip install 闇€重新下载 | |
| uv cache | Python 包需重新下载 | 鍙兘闈炲父澶?|
| NuGet packages | .NET 项Ŀ鎭㈠变慢 | |
| Conda packages | 鐜创建闇€重新下载 | |
| torch/huggingface cache | AI 妯″瀷闇€重新下载 | 鍙兘闇€Ҫ数Сʱ |

### [KEEP] 寤鸿保留的项鐩?

| 项Ŀ | ԭ因 |
|------|------|
| Docker volumes | 鍙兘鍖呭惈鏁版嵁搴撴暟鎹?|
| VS Code extensions | 闇€Ҫ重新安װ配缃?|
| 娴忚鍣ㄩ厤缃枃浠?| 包含涔︾、密码等 |
| SSH keys (.ssh) | 密Կ文件 |

## 宸ヤ綔娴佺▼

### 绗竴姝ワ細杩愯分析脚本

1. д入 `disk_overview.ps1` -> 鎵ц -> 获ȡ磁盘姒傝
2. д入 `user_folders.ps1` -> 鎵ц -> 获ȡ鐢ㄦ埛鏂囦欢澶逛俊鎭?
3. д入 `appdata_analysis.ps1` -> 鎵ц -> 获ȡ AppData 分析锛?*鍙兘鑰楁椂杈冮暱锛岃缃?timeout 300000+**锛?
4. д入 `dev_caches.ps1` -> 鎵ц -> 获ȡ寮€鍙戣€呯紦瀛樺垎鏋?

ÿ个脚本鎵ц后ɾ闄ゃ€?

### 绗簩姝ワ細鏁寸悊骞跺憟鐜板彂鐜?

鎸?[SAFE] / [TRADEOFF] / [KEEP] 分类呈现，包鍚細
- 项Ŀ鍚嶇О鍜屽ぇ灏?
- ɾ除后果˵明
- 寤鸿的清鐞嗛€夐」

### 绗笁姝ワ細鐢ㄦ埛纭后ִ行清鐞?

根据鐢ㄦ埛閫夋嫨鐨勯€夐」锛?
- A) 鎵ц安ȫ清理：运行相Ӧ的清理脚本
- B) 鏌ョ湅鏇村详情：深鍏ュ垎鏋愮壒瀹氭枃浠跺す
- C) 清理特定项Ŀ：ȷ璁ゅ悗鎵ц

### 绗洓姝ワ細楠岃瘉缁撴灉

```bash
powershell -NoProfile -Command "(Get-PSDrive C).Free / 1GB"
```

对比清理ǰ后的可鐢ㄧ┖闂淬€?

## 鎶ュ憡鏍煎紡妯℃澘

```markdown
## 磁盘分析鎶ュ憡

**C: 鐩?*: XX GB 已用 / XX GB 鎬诲閲?(XX% ʹ用率，XX GB 鍙敤)

---

### [SAFE] 鍙畨鍏ㄦ竻鐞?(~X GB)

| 项Ŀ | 大小 | ɾ除后果 |
|------|------|----------|
| 回收绔?| X MB | 鏃?|
| 鏃х増 Playwright | X GB | 无，保留鏈€新版鏈?|
| npm _npx | X GB | npx 重新下载 |

---

### [TRADEOFF] 闇€Ҫ您决定

| 项Ŀ | 大小 | ɾ除后果 |
|------|------|----------|
| uv cache | XX GB | Python 包需重新下载 |
| npm _cacache | X GB | npm install 闇€重新下载 |

---

### [KEEP] 寤鸿保留

| 项Ŀ | 大小 | ԭ因 |
|------|------|------|
| NuGet packages | X GB | 避免閲嶅下载 |
| Docker | XX GB | 鍙兘鍖呭惈閲嶈数据 |

---

### 寤鸿操作

- **A)** 鎵ц安ȫ清理 (~X GB)
- **B)** 鏌ョ湅鏇村详情
- **C)** 清理特定项Ŀ（需纭锛?
```

## 娉ㄦ剰浜嬮」

1. **脚本鎵ц超ʱ**锛氬ぇ文件夹ɨ描可能需Ҫ几分钟锛岃缃?timeout 涓?300000ms (5分钟) 或更闀?
2. **璺緞鍙樹綋**：ĳЩ缓存可能在 LOCALAPPDATA 鎴?APPDATA，需Ҫ都妫€鏌?
3. **编码闂**：PowerShell 涓枃閿欒淇℃伅鍙兘鏄剧ず乱码，不Ӱ响功能
4. **Ȩ限闂**：ϵͳ文浠跺す闇€瑕佺理ԱȨ限
5. **清理后验璇?*锛氬缁堝比清理ǰ后的鍙敤绌洪棿
6. **脚本清理**：ִ行完毕后ɾ除临ʱ脚本文件

## 绂佹操作

- 涓嶈ʹ用 `docker volume prune -f` 鎴?`docker system prune -a --volumes`
- 涓嶈ɾ除鐢ㄦ埛鏂囨。銆佹闈€佸浘鐗囩瓑涓汉鏂囦欢澶?
- 涓嶈ɾ除 .ssh、֤书等敏感文件
- 涓嶈鍦ㄦ湭纭的情况下ɾ除澶у瀷缂撳瓨
