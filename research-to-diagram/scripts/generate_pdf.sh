#!/bin/bash
# Generate PDF from DOT file using Graphviz
# 自动查找并使用 Graphviz，支持跨平台

set -e

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 查找 Graphviz dot 命令
find_dot_command() {
    local dot_path=""

    # 首先检查 PATH
    if command -v dot &> /dev/null; then
        dot_path=$(command -v dot)
        echo "$dot_path"
        return 0
    fi

    # 检测操作系统
    local OS="$(uname -s)"
    case "$OS" in
        Linux*)     local OS_TYPE="Linux";;
        Darwin*)    local OS_TYPE="macOS";;
        MINGW*|MSYS*|CYGWIN*) local OS_TYPE="Windows";;
        *)          local OS_TYPE="Unknown";;
    esac

    # 如果 PATH 中没有，搜索常见安装位置
    case "$OS_TYPE" in
        "Windows")
            # Windows 常见位置
            local search_paths=(
                "/c/Program Files/Graphviz/bin/dot.exe"
                "/c/Program Files (x86)/Graphviz/bin/dot.exe"
            )

            for path in "${search_paths[@]}"; do
                if [ -f "$path" ]; then
                    echo "$path"
                    return 0
                fi
            done

            # 尝试使用 PowerShell 搜索
            if command -v powershell &> /dev/null; then
                local ps_path
                ps_path=$(powershell -Command "Get-ChildItem 'C:\Program Files' -Filter 'dot.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName" 2>/dev/null)
                if [ -n "$ps_path" ] && [ -f "$ps_path" ]; then
                    echo "$ps_path"
                    return 0
                fi
            fi
            ;;

        "macOS")
            # macOS 常见位置
            local search_paths=(
                "/usr/local/bin/dot"
                "/opt/homebrew/bin/dot"
                "$HOME/.brew/bin/dot"
            )

            for path in "${search_paths[@]}"; do
                if [ -f "$path" ]; then
                    echo "$path"
                    return 0
                fi
            done
            ;;

        "Linux")
            # Linux 常见位置
            local search_paths=(
                "/usr/bin/dot"
                "/usr/local/bin/dot"
                "$HOME/.local/bin/dot"
            )

            for path in "${search_paths[@]}"; do
                if [ -f "$path" ]; then
                    echo "$path"
                    return 0
                fi
            done
            ;;
    esac

    return 1
}

# 显示用法
usage() {
    cat << EOF
Usage: $0 <input.dot> [output.pdf] [output.png]

Generate PDF/PNG from Graphviz DOT file.

Arguments:
  input.dot    Input DOT file path (required)
  output.pdf   Output PDF file path (optional, defaults to same name as input)
  output.png   Output PNG file path (optional, generates PNG alongside PDF)

Examples:
  $0 diagram.dot
  $0 diagram.dot output.pdf
  $0 diagram.dot output.pdf output.png

Options:
  --png-only   Only generate PNG, skip PDF
  --pdf-only   Only generate PDF (default)

Requirements:
  - Graphviz must be installed

Installation:
  - macOS:   brew install graphviz
  - Ubuntu:  sudo apt-get install graphviz
  - Windows: winget install Graphviz.Graphviz
             or download from https://graphviz.org/download/
EOF
    exit 1
}

# 解析参数
GENERATE_PNG=true
GENERATE_PDF=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --png-only)
            GENERATE_PDF=false
            shift
            ;;
        --pdf-only)
            GENERATE_PNG=false
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            break
            ;;
    esac
done

# 检查参数
if [ $# -lt 1 ]; then
    echo "Error: Missing input file"
    usage
fi

INPUT_DOT="$1"
OUTPUT_PDF="${2:-${INPUT_DOT%.dot}.pdf}"

# 如果指定了第三个参数，使用它作为 PNG 输出路径
if [ $# -ge 3 ]; then
    OUTPUT_PNG="$3"
else
    # 否则基于 PDF 路径生成 PNG 路径
    OUTPUT_PNG="${OUTPUT_PDF%.pdf}.png"
fi

# 检查输入文件是否存在
if [ ! -f "$INPUT_DOT" ]; then
    echo "Error: Input file '$INPUT_DOT' not found"
    exit 1
fi

# 查找 Graphviz dot 命令
DOT_CMD=$(find_dot_command)

if [ -z "$DOT_CMD" ]; then
    echo "Error: Graphviz is not installed or not found in PATH"
    echo ""
    echo "Installation instructions:"
    echo "  macOS:   brew install graphviz"
    echo "  Ubuntu:  sudo apt-get install graphviz"
    echo "  Windows: winget install Graphviz.Graphviz"
    echo "           or download from https://graphviz.org/download/"
    exit 1
fi

echo "Found Graphviz at: $DOT_CMD"

# 验证 DOT 文件语法
echo "Validating DOT file syntax..."
if ! "$DOT_CMD" -Tpdf "$INPUT_DOT" -o /dev/null 2>&1; then
    echo "Warning: DOT file has validation issues, but will attempt to generate output"
fi

# 生成 PDF
if [ "$GENERATE_PDF" = true ]; then
    echo "Generating PDF: $OUTPUT_PDF"

    # 如果文件存在，先删除以避免权限问题
    if [ -f "$OUTPUT_PDF" ]; then
        rm -f "$OUTPUT_PDF" 2>/dev/null || true
    fi

    "$DOT_CMD" -Tpdf "$INPUT_DOT" -o "$OUTPUT_PDF" 2>&1

    # 检查生成是否成功
    if [ -f "$OUTPUT_PDF" ]; then
        FILE_SIZE=$(du -h "$OUTPUT_PDF" | cut -f1)
        echo "✓ PDF generated successfully: $OUTPUT_PDF ($FILE_SIZE)"
    else
        echo "✗ Failed to generate PDF (file may be locked or in use)"
        echo "  Close the file if it's open and try again"
        # 不退出，继续尝试生成 PNG
    fi
fi

# 生成 PNG
if [ "$GENERATE_PNG" = true ]; then
    echo "Generating PNG: $OUTPUT_PNG"

    # 如果文件存在，先删除以避免权限问题
    if [ -f "$OUTPUT_PNG" ]; then
        rm -f "$OUTPUT_PNG" 2>/dev/null || true
    fi

    "$DOT_CMD" -Tpng "$INPUT_DOT" -o "$OUTPUT_PNG" 2>&1

    # 检查生成是否成功
    if [ -f "$OUTPUT_PNG" ]; then
        FILE_SIZE=$(du -h "$OUTPUT_PNG" | cut -f1)
        echo "✓ PNG generated successfully: $OUTPUT_PNG ($FILE_SIZE)"
    else
        echo "✗ Failed to generate PNG (file may be locked or in use)"
        echo "  Close the file if it's open and try again"
        # 只有当两个都失败时才退出
        if [ "$GENERATE_PDF" = true ] && [ ! -f "$OUTPUT_PDF" ]; then
            exit 1
        fi
    fi
fi

echo ""
echo "Done! Output files:"
[ "$GENERATE_PDF" = true ] && [ -f "$OUTPUT_PDF" ] && echo "  - PDF: $OUTPUT_PDF"
[ "$GENERATE_PNG" = true ] && [ -f "$OUTPUT_PNG" ] && echo "  - PNG: $OUTPUT_PNG"
