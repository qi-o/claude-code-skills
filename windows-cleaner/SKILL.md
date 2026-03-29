---
name: windows-cleaner
description: Analyze and reclaim Windows disk space through intelligent cleanup recommendations. Use when users report disk space issues, need to clean up their Windows PC, or want to understand what's consuming storage. Use when user says "清理磁盘", "磁盘空间", "disk cleanup", "C盘满了", "释放空间", or "storage analysis". Do NOT use on non-Windows systems or for application-specific cleanup.
license: MIT
allowed-tools: "Bash(powershell:*) Read"
version: 0.1.0
metadata:
  category: domain-specific
---

# Windows Cleaner

## Overview

分析 Windows 磁盘使用情况，提供安全的清理建议。遵循**安全优先**原则：先分析，再确认，最后执行。

## 核心原则

1. **安全第一**：删除操作必须用户确认
2. **价值优先**：不为数字好看而删除有用的缓存
3. **网络环境意识**：考虑重新下载的时间成本
4. **影响分析**：每个清理建议必须说明删除后果

## 技术要点：PowerShell 执行方式

**关键**：复杂 PowerShell 命令必须写成 `.ps1` 脚本文件执行，不能内联执行。

### 正确方式

```bash
# 1. 使用 Write 工具写入脚本文件
# Write tool -> C:\Users\USERNAME\script.ps1

# 2. 执行脚本
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\USERNAME\script.ps1"

# 3. 删除脚本
rm -f "C:\Users\USERNAME\script.ps1"
```

### 错误方式（会因转义问题失败）

```bash
# 这些会失败：
powershell -Command "Get-PSDrive | Select-Object @{N='Size';E={$_.Used}}"  # 失败
powershell -Command "$arr = @('a','b'); foreach ($i in $arr) { ... }"      # 失败
powershell -Command "... $_.Property ..."                                   # 失败
```

### 简单命令可以内联

```bash
# 这些简单命令可以内联：
powershell -NoProfile -Command "(Get-PSDrive C).Free / 1GB"
powershell -NoProfile -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
powershell -NoProfile -Command "Test-Path 'C:\some\path'"
powershell -NoProfile -Command "Remove-Item -Path 'C:\path' -Recurse -Force"
```

## 分析脚本模板

### 脚本 1：磁盘概览 (disk_overview.ps1)

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

### 脚本 2：用户文件夹分析 (user_folders.ps1)

```powershell
Write-Host "=== User Temp Folder ===" -ForegroundColor Yellow
$tempPath = $env:TEMP
if (Test-Path $tempPath) {
    $tempSize = (Get-ChildItem -Path $tempPath -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Write-Host "User Temp: $([math]::Round($tempSize/1GB, 2)) GB"
}

Write-Host "`n=== Downloads Folder ===" -ForegroundColor Yellow
# 重要：使用 $env:USERPROFILE\Downloads，不要用 [Environment]::GetFolderPath("Downloads")
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

### 脚本 3：AppData 大文件夹分析 (appdata_analysis.ps1)

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

### 脚本 4：开发者缓存分析 (dev_caches.ps1)

```powershell
Write-Host "=== Developer Caches ===" -ForegroundColor Cyan

# 定义要检查的缓存路径（每个缓存可能有多个位置）
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

## 清理脚本模板

### 清理 Playwright 旧版本 (cleanup_playwright.ps1)

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

## 清理分类表

### [SAFE] 安全清理项目

| 项目 | 影响 | 清理方式 |
|------|------|----------|
| 回收站 | 无 | `Clear-RecycleBin -Force` |
| 旧版 Playwright 浏览器 | 无（保留最新版本） | cleanup_playwright.ps1 |
| npm _npx 缓存 | npx 下次使用时重新下载 | cleanup_npx.ps1 |
| puppeteer 缓存 | 需要时重新下载 | cleanup_puppeteer.ps1 |
| 超过7天的 Temp 文件 | 无 | 脚本或 cleanmgr |
| Windows Update 缓存 | 无（需管理员权限） | cleanmgr |

### [TRADEOFF] 需确认的清理项目

| 项目 | 影响 | 备注 |
|------|------|------|
| npm _cacache | npm install 需重新下载 | 国内网络较慢 |
| pip cache | pip install 需重新下载 | |
| uv cache | Python 包需重新下载 | 可能非常大 |
| NuGet packages | .NET 项目恢复变慢 | |
| Conda packages | 环境创建需重新下载 | |
| torch/huggingface cache | AI 模型需重新下载 | 可能需要数小时 |

### [KEEP] 建议保留的项目

| 项目 | 原因 |
|------|------|
| Docker volumes | 可能包含数据库数据 |
| VS Code extensions | 需要重新安装配置 |
| 浏览器配置文件 | 包含书签、密码等 |
| SSH keys (.ssh) | 密钥文件 |

## 工作流程

### 第一步：运行分析脚本

1. 写入 `disk_overview.ps1` -> 执行 -> 获取磁盘概览
2. 写入 `user_folders.ps1` -> 执行 -> 获取用户文件夹信息
3. 写入 `appdata_analysis.ps1` -> 执行 -> 获取 AppData 分析（**可能耗时较长，设置 timeout 300000+**）
4. 写入 `dev_caches.ps1` -> 执行 -> 获取开发者缓存分析

每个脚本执行后删除。

### 第二步：整理并呈现发现

按 [SAFE] / [TRADEOFF] / [KEEP] 分类呈现，包含：
- 项目名称和大小
- 删除后果说明
- 建议的清理选项

### 第三步：用户确认后执行清理

根据用户选择的选项：
- A) 执行安全清理：运行相应的清理脚本
- B) 查看更多详情：深入分析特定文件夹
- C) 清理特定项目：确认后执行

### 第四步：验证结果

```bash
powershell -NoProfile -Command "(Get-PSDrive C).Free / 1GB"
```

对比清理前后的可用空间。

## 报告格式模板

```markdown
## 磁盘分析报告

**C: 盘**: XX GB 已用 / XX GB 总容量 (XX% 使用率，XX GB 可用)

---

### [SAFE] 可安全清理 (~X GB)

| 项目 | 大小 | 删除后果 |
|------|------|----------|
| 回收站 | X MB | 无 |
| 旧版 Playwright | X GB | 无，保留最新版本 |
| npm _npx | X GB | npx 重新下载 |

---

### [TRADEOFF] 需要您决定

| 项目 | 大小 | 删除后果 |
|------|------|----------|
| uv cache | XX GB | Python 包需重新下载 |
| npm _cacache | X GB | npm install 需重新下载 |

---

### [KEEP] 建议保留

| 项目 | 大小 | 原因 |
|------|------|------|
| NuGet packages | X GB | 避免重复下载 |
| Docker | XX GB | 可能包含重要数据 |

---

### 建议操作

- **A)** 执行安全清理 (~X GB)
- **B)** 查看更多详情
- **C)** 清理特定项目（需确认）
```

## 注意事项

1. **脚本执行超时**：大文件夹扫描可能需要几分钟，设置 timeout 为 300000ms (5分钟) 或更长
2. **路径变量**：某些缓存可能在 LOCALAPPDATA 或 APPDATA，需要都检查
3. **编码问题**：PowerShell 中文错误信息可能显示乱码，不影响功能
4. **权限问题**：系统文件夹需要管理员权限
5. **清理后验证**：始终对比清理前后的可用空间
6. **脚本清理**：执行完毕后删除临时脚本文件

## 禁止操作

- 不要使用 `docker volume prune -f` 或 `docker system prune -a --volumes`
- 不要删除用户文档、桌面、图片等个人文件夹
- 不要删除 .ssh、证书等敏感文件
- 不要在未确认的情况下删除大型缓存
