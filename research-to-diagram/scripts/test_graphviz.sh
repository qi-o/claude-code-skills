#!/bin/bash
# Test script to verify Graphviz detection and generation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOT_FILE="$SCRIPT_DIR/test.dot"

# 创建一个简单的测试 DOT 文件
cat > "$DOT_FILE" << 'EOF'
digraph Test {
    fontname="Microsoft YaHei, Arial Unicode MS, SimHei"
    node [fontname="Microsoft YaHei, Arial Unicode MS, SimHei"]
    edge [fontname="Microsoft YaHei, Arial Unicode MS, SimHei"]

    A [label="开始"]
    B [label="处理"]
    C [label="完成"]

    A -> B [label="执行"]
    B -> C [label="成功"]
}
EOF

echo "Testing Graphviz detection and PDF generation..."
echo ""

# 运行生成脚本
bash "$SCRIPT_DIR/generate_pdf.sh" "$DOT_FILE" "$SCRIPT_DIR/test_output.pdf"

# 清理测试文件
rm -f "$DOT_FILE"

echo ""
echo "Test completed!"
