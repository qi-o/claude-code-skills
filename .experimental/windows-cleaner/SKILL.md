---
name: windows-cleaner
description: Analyze and reclaim Windows disk space through intelligent cleanup recommendations. Use when users report disk space issues, need to clean up their Windows PC, or want to understand what's consuming storage. Use when user says "娓呯悊纾佺洏", "纾佺洏绌洪棿", "disk cleanup", "C鐩樻弧浜?, "閲婃斁绌洪棿", or "storage analysis".
license: MIT
allowed-tools: "Bash(powershell:*) Read"
version: 0.1.0
metadata:
  category: domain-specific
---

# Windows Cleaner

## Overview

鍒嗘瀽 Windows 纾佺洏浣跨敤鎯呭喌锛屾彁渚涘畨鍏ㄧ殑娓呯悊寤鸿銆傞伒寰?*瀹夊叏浼樺厛**鍘熷垯锛氬厛鍒嗘瀽锛屽啀纭锛屾渶鍚庢墽琛屻€?

## 鏍稿績鍘熷垯

1. **瀹夊叏绗竴**锛氬垹闄ゆ搷浣滃繀椤荤敤鎴风‘璁?
2. **浠峰€间紭鍏?*锛氫笉涓轰簡鏁板瓧濂界湅鑰屽垹闄ゆ湁鐢ㄧ殑缂撳瓨
3. **缃戠粶鐜鎰忚瘑**锛氳€冭檻閲嶆柊涓嬭浇鐨勬椂闂存垚鏈?
4. **褰卞搷鍒嗘瀽**锛氭瘡涓竻鐞嗗缓璁繀椤昏鏄庡垹闄ゅ悗鏋?

## 鎶€鏈鐐癸細PowerShell 鎵ц鏂瑰紡

**鍏抽敭**锛氬鏉?PowerShell 鍛戒护蹇呴』鍐欐垚 `.ps1` 鑴氭湰鏂囦欢鎵ц锛屼笉鑳藉唴鑱旀墽琛屻€?

### 姝ｇ‘鏂瑰紡

```bash
# 1. 浣跨敤 Write 宸ュ叿鍐欏叆鑴氭湰鏂囦欢
# Write tool -> C:\Users\USERNAME\script.ps1

# 2. 鎵ц鑴氭湰
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\USERNAME\script.ps1"

# 3. 鍒犻櫎鑴氭湰
rm -f "C:\Users\USERNAME\script.ps1"
```

### 閿欒鏂瑰紡锛堜細鍥犺浆涔夐棶棰樺け璐ワ級

```bash
# 杩欎簺浼氬け璐ワ細
powershell -Command "Get-PSDrive | Select-Object @{N='Size';E={$_.Used}}"  # 澶辫触
powershell -Command "$arr = @('a','b'); foreach ($i in $arr) { ... }"      # 澶辫触
powershell -Command "... $_.Property ..."                                   # 澶辫触
```

### 绠€鍗曞懡浠ゅ彲浠ュ唴鑱?

```bash
# 杩欎簺绠€鍗曞懡浠ゅ彲浠ュ唴鑱旓細
powershell -NoProfile -Command "(Get-PSDrive C).Free / 1GB"
powershell -NoProfile -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
powershell -NoProfile -Command "Test-Path 'C:\some\path'"
powershell -NoProfile -Command "Remove-Item -Path 'C:\path' -Recurse -Force"
```

## 鍒嗘瀽鑴氭湰妯℃澘

### 鑴氭湰 1锛氱鐩樻瑙?(disk_overview.ps1)

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

### 鑴氭湰 2锛氱敤鎴锋枃浠跺す鍒嗘瀽 (user_folders.ps1)

```powershell
Write-Host "=== User Temp Folder ===" -ForegroundColor Yellow
$tempPath = $env:TEMP
if (Test-Path $tempPath) {
    $tempSize = (Get-ChildItem -Path $tempPath -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Write-Host "User Temp: $([math]::Round($tempSize/1GB, 2)) GB"
}

Write-Host "`n=== Downloads Folder ===" -ForegroundColor Yellow
# 閲嶈锛氫娇鐢?$env:USERPROFILE\Downloads锛屼笉瑕佺敤 [Environment]::GetFolderPath("Downloads")
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

### 鑴氭湰 3锛欰ppData 澶ф枃浠跺す鍒嗘瀽 (appdata_analysis.ps1)

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

### 鑴氭湰 4锛氬紑鍙戣€呯紦瀛樺垎鏋?(dev_caches.ps1)

```powershell
Write-Host "=== Developer Caches ===" -ForegroundColor Cyan

# 瀹氫箟瑕佹鏌ョ殑缂撳瓨璺緞锛堟瘡涓紦瀛樺彲鑳芥湁澶氫釜浣嶇疆锛?
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

## 娓呯悊鑴氭湰妯℃澘

### 娓呯悊 Playwright 鏃х増鏈?(cleanup_playwright.ps1)

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

### 娓呯悊 npm _npx 缂撳瓨 (cleanup_npx.ps1)

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

### 娓呯悊 puppeteer 缂撳瓨 (cleanup_puppeteer.ps1)

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

## 娓呯悊鍒嗙被琛?

### [SAFE] 瀹夊叏娓呯悊椤圭洰

| 椤圭洰 | 褰卞搷 | 娓呯悊鏂瑰紡 |
|------|------|----------|
| 鍥炴敹绔?| 鏃?| `Clear-RecycleBin -Force` |
| 鏃х増 Playwright 娴忚鍣?| 鏃狅紙淇濈暀鏈€鏂扮増鏈級 | cleanup_playwright.ps1 |
| npm _npx 缂撳瓨 | npx 涓嬫浣跨敤鏃堕噸鏂颁笅杞?| cleanup_npx.ps1 |
| puppeteer 缂撳瓨 | 闇€瑕佹椂閲嶆柊涓嬭浇 | cleanup_puppeteer.ps1 |
| 瓒呰繃7澶╃殑 Temp 鏂囦欢 | 鏃?| 鑴氭湰鎴?cleanmgr |
| Windows Update 缂撳瓨 | 鏃狅紙闇€绠＄悊鍛樻潈闄愶級 | cleanmgr |

### [TRADEOFF] 闇€纭鐨勬竻鐞嗛」鐩?

| 椤圭洰 | 褰卞搷 | 澶囨敞 |
|------|------|------|
| npm _cacache | npm install 闇€閲嶆柊涓嬭浇 | 鍥藉唴缃戠粶杈冩參 |
| pip cache | pip install 闇€閲嶆柊涓嬭浇 | |
| uv cache | Python 鍖呴渶閲嶆柊涓嬭浇 | 鍙兘闈炲父澶?|
| NuGet packages | .NET 椤圭洰鎭㈠鍙樻參 | |
| Conda packages | 鐜鍒涘缓闇€閲嶆柊涓嬭浇 | |
| torch/huggingface cache | AI 妯″瀷闇€閲嶆柊涓嬭浇 | 鍙兘闇€瑕佹暟灏忔椂 |

### [KEEP] 寤鸿淇濈暀鐨勯」鐩?

| 椤圭洰 | 鍘熷洜 |
|------|------|
| Docker volumes | 鍙兘鍖呭惈鏁版嵁搴撴暟鎹?|
| VS Code extensions | 闇€瑕侀噸鏂板畨瑁呴厤缃?|
| 娴忚鍣ㄩ厤缃枃浠?| 鍖呭惈涔︾銆佸瘑鐮佺瓑 |
| SSH keys (.ssh) | 瀵嗛挜鏂囦欢 |

## 宸ヤ綔娴佺▼

### 绗竴姝ワ細杩愯鍒嗘瀽鑴氭湰

1. 鍐欏叆 `disk_overview.ps1` -> 鎵ц -> 鑾峰彇纾佺洏姒傝
2. 鍐欏叆 `user_folders.ps1` -> 鎵ц -> 鑾峰彇鐢ㄦ埛鏂囦欢澶逛俊鎭?
3. 鍐欏叆 `appdata_analysis.ps1` -> 鎵ц -> 鑾峰彇 AppData 鍒嗘瀽锛?*鍙兘鑰楁椂杈冮暱锛岃缃?timeout 300000+**锛?
4. 鍐欏叆 `dev_caches.ps1` -> 鎵ц -> 鑾峰彇寮€鍙戣€呯紦瀛樺垎鏋?

姣忎釜鑴氭湰鎵ц鍚庡垹闄ゃ€?

### 绗簩姝ワ細鏁寸悊骞跺憟鐜板彂鐜?

鎸?[SAFE] / [TRADEOFF] / [KEEP] 鍒嗙被鍛堢幇锛屽寘鍚細
- 椤圭洰鍚嶇О鍜屽ぇ灏?
- 鍒犻櫎鍚庢灉璇存槑
- 寤鸿鐨勬竻鐞嗛€夐」

### 绗笁姝ワ細鐢ㄦ埛纭鍚庢墽琛屾竻鐞?

鏍规嵁鐢ㄦ埛閫夋嫨鐨勯€夐」锛?
- A) 鎵ц瀹夊叏娓呯悊锛氳繍琛岀浉搴旂殑娓呯悊鑴氭湰
- B) 鏌ョ湅鏇村璇︽儏锛氭繁鍏ュ垎鏋愮壒瀹氭枃浠跺す
- C) 娓呯悊鐗瑰畾椤圭洰锛氱‘璁ゅ悗鎵ц

### 绗洓姝ワ細楠岃瘉缁撴灉

```bash
powershell -NoProfile -Command "(Get-PSDrive C).Free / 1GB"
```

瀵规瘮娓呯悊鍓嶅悗鐨勫彲鐢ㄧ┖闂淬€?

## 鎶ュ憡鏍煎紡妯℃澘

```markdown
## 纾佺洏鍒嗘瀽鎶ュ憡

**C: 鐩?*: XX GB 宸茬敤 / XX GB 鎬诲閲?(XX% 浣跨敤鐜囷紝XX GB 鍙敤)

---

### [SAFE] 鍙畨鍏ㄦ竻鐞?(~X GB)

| 椤圭洰 | 澶у皬 | 鍒犻櫎鍚庢灉 |
|------|------|----------|
| 鍥炴敹绔?| X MB | 鏃?|
| 鏃х増 Playwright | X GB | 鏃狅紝淇濈暀鏈€鏂扮増鏈?|
| npm _npx | X GB | npx 閲嶆柊涓嬭浇 |

---

### [TRADEOFF] 闇€瑕佹偍鍐冲畾

| 椤圭洰 | 澶у皬 | 鍒犻櫎鍚庢灉 |
|------|------|----------|
| uv cache | XX GB | Python 鍖呴渶閲嶆柊涓嬭浇 |
| npm _cacache | X GB | npm install 闇€閲嶆柊涓嬭浇 |

---

### [KEEP] 寤鸿淇濈暀

| 椤圭洰 | 澶у皬 | 鍘熷洜 |
|------|------|------|
| NuGet packages | X GB | 閬垮厤閲嶅涓嬭浇 |
| Docker | XX GB | 鍙兘鍖呭惈閲嶈鏁版嵁 |

---

### 寤鸿鎿嶄綔

- **A)** 鎵ц瀹夊叏娓呯悊 (~X GB)
- **B)** 鏌ョ湅鏇村璇︽儏
- **C)** 娓呯悊鐗瑰畾椤圭洰锛堥渶纭锛?
```

## 娉ㄦ剰浜嬮」

1. **鑴氭湰鎵ц瓒呮椂**锛氬ぇ鏂囦欢澶规壂鎻忓彲鑳介渶瑕佸嚑鍒嗛挓锛岃缃?timeout 涓?300000ms (5鍒嗛挓) 鎴栨洿闀?
2. **璺緞鍙樹綋**锛氭煇浜涚紦瀛樺彲鑳藉湪 LOCALAPPDATA 鎴?APPDATA锛岄渶瑕侀兘妫€鏌?
3. **缂栫爜闂**锛歅owerShell 涓枃閿欒淇℃伅鍙兘鏄剧ず涔辩爜锛屼笉褰卞搷鍔熻兘
4. **鏉冮檺闂**锛氱郴缁熸枃浠跺す闇€瑕佺鐞嗗憳鏉冮檺
5. **娓呯悊鍚庨獙璇?*锛氬缁堝姣旀竻鐞嗗墠鍚庣殑鍙敤绌洪棿
6. **鑴氭湰娓呯悊**锛氭墽琛屽畬姣曞悗鍒犻櫎涓存椂鑴氭湰鏂囦欢

## 绂佹鎿嶄綔

- 涓嶈浣跨敤 `docker volume prune -f` 鎴?`docker system prune -a --volumes`
- 涓嶈鍒犻櫎鐢ㄦ埛鏂囨。銆佹闈€佸浘鐗囩瓑涓汉鏂囦欢澶?
- 涓嶈鍒犻櫎 .ssh銆佽瘉涔︾瓑鏁忔劅鏂囦欢
- 涓嶈鍦ㄦ湭纭鐨勬儏鍐典笅鍒犻櫎澶у瀷缂撳瓨
