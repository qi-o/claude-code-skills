#!/bin/bash
# Find Graphviz installation across different platforms

set -e

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "Linux";;
        Darwin*)    echo "macOS";;
        MINGW*|MSYS*|CYGWIN*) echo "Windows";;
        *)          echo "Unknown";;
    esac
}

OS=$(detect_os)

# 查找 Graphviz 的 dot 命令
find_dot_command() {
    local dot_path=""

    # 首先检查 PATH
    if command -v dot &> /dev/null; then
        dot_path=$(command -v dot)
        echo "$dot_path"
        return 0
    fi

    # 如果 PATH 中没有，搜索常见安装位置
    case "$OS" in
        "Windows")
            # Windows 常见位置
            local search_paths=(
                "/c/Program Files/Graphviz/bin/dot.exe"
                "/c/Program Files (x86)/Graphviz/bin/dot.exe"
                "$LOCALAPPDATA/Programs/Graphviz/bin/dot.exe"
                "$APPDATA/Graphviz/bin/dot.exe"
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
                ps_path=$(powershell -Command "Get-Command dot -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source" 2>/dev/null | head -1)
                if [ -n "$ps_path" ]; then
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

# 主函数
main() {
    if [ "$1" = "--export-path" ]; then
        # 输出可用于导出的路径
        local dot_cmd
        dot_cmd=$(find_dot_command)

        if [ -n "$dot_cmd" ]; then
            # 获取 dot 所在的目录
            local dot_dir
            dot_dir=$(dirname "$dot_cmd")
            echo "$dot_dir"
            exit 0
        else
            exit 1
        fi
    else
        # 输出完整路径
        local dot_cmd
        dot_cmd=$(find_dot_command)

        if [ -n "$dot_cmd" ]; then
            echo "$dot_cmd"
            exit 0
        else
            exit 1
        fi
    fi
}

main "$@"
