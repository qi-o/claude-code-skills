#!/bin/bash

# Sync to GitHub - 同步 Claude Code 技能和配置到 GitHub 仓库
# 使用方法: bash sync.sh

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 仓库路径
SKILLS_REPO="$HOME/claude-code-skills"
CONFIG_REPO="$HOME/claude-code-config"
CLAUDE_DIR="$HOME/.claude"

echo -e "${BLUE}🚀 开始同步 Claude Code 配置和技能到 GitHub...${NC}\n"

# ============================================
# 1. 检查仓库是否存在
# ============================================
echo -e "${YELLOW}📋 检查仓库...${NC}"

if [ ! -d "$SKILLS_REPO/.git" ]; then
    echo -e "${RED}❌ 错误: claude-code-skills 仓库不存在${NC}"
    echo -e "请先克隆仓库: git clone https://github.com/qi-o/claude-code-skills.git ~/claude-code-skills"
    exit 1
fi

if [ ! -d "$CONFIG_REPO/.git" ]; then
    echo -e "${RED}❌ 错误: claude-code-config 仓库不存在${NC}"
    echo -e "请先克隆仓库: git clone https://github.com/qi-o/claude-code-config.git ~/claude-code-config"
    exit 1
fi

echo -e "${GREEN}✓ 仓库检查通过${NC}\n"

# ============================================
# 2. 同步技能到 claude-code-skills
# ============================================
echo -e "${YELLOW}📦 同步技能目录...${NC}"

# 使用 cp 命令同步（Windows Git Bash 兼容）
cp -r "$CLAUDE_DIR/skills/"* "$SKILLS_REPO/" 2>/dev/null || true

echo -e "${GREEN}✓ 技能同步完成${NC}\n"

# ============================================
# 3. 同步配置到 claude-code-config
# ============================================
echo -e "${YELLOW}⚙️  同步配置文件...${NC}"

# 同步根目录文件
cp "$CLAUDE_DIR/CLAUDE.md" "$CONFIG_REPO/" 2>/dev/null || true
cp "$CLAUDE_DIR/settings.json" "$CONFIG_REPO/" 2>/dev/null || true

# 同步目录（Windows Git Bash 兼容）
for dir in agents commands hooks plugins rules; do
    if [ -d "$CLAUDE_DIR/$dir" ]; then
        # 删除目标目录并重新复制
        rm -rf "$CONFIG_REPO/$dir"
        cp -r "$CLAUDE_DIR/$dir" "$CONFIG_REPO/"
    fi
done

echo -e "${GREEN}✓ 配置同步完成${NC}\n"

# ============================================
# 4. 清理敏感信息
# ============================================
echo -e "${YELLOW}🔒 清理敏感信息...${NC}"

if [ -f "$CONFIG_REPO/settings.json" ]; then
    # 使用 sed 替换 API token（兼容 macOS 和 Linux）
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' 's/"ANTHROPIC_AUTH_TOKEN": "sk-[^"]*"/"ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY_HERE"/g' "$CONFIG_REPO/settings.json"
    else
        # Linux/Windows Git Bash
        sed -i 's/"ANTHROPIC_AUTH_TOKEN": "sk-[^"]*"/"ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY_HERE"/g' "$CONFIG_REPO/settings.json"
    fi
    echo -e "${GREEN}✓ 敏感信息已清理${NC}\n"
fi

# ============================================
# 5. 提交更改
# ============================================
echo -e "${YELLOW}💾 提交更改...${NC}"

# 提交技能仓库
cd "$SKILLS_REPO"
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${BLUE}ℹ️  技能仓库无更改，跳过提交${NC}"
    SKILLS_COMMITTED=false
else
    git add -A
    git commit -m "$(cat <<'EOF'
同步技能更新

- 更新现有技能
- 添加新技能（如有）
- 删除已移除的技能
EOF
)"
    echo -e "${GREEN}✓ 技能仓库已提交${NC}"
    SKILLS_COMMITTED=true
fi

# 提交配置仓库
cd "$CONFIG_REPO"
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${BLUE}ℹ️  配置仓库无更改，跳过提交${NC}"
    CONFIG_COMMITTED=false
else
    git add -A
    git commit -m "$(cat <<'EOF'
同步配置更新

- 更新 CLAUDE.md 和 settings.json
- 同步 agents, commands, hooks, plugins, rules
- 清理敏感信息
EOF
)"
    echo -e "${GREEN}✓ 配置仓库已提交${NC}"
    CONFIG_COMMITTED=true
fi

echo ""

# ============================================
# 6. 显示推送提示
# ============================================
echo -e "${GREEN}✅ 同步完成！${NC}\n"

if [ "$SKILLS_COMMITTED" = true ] || [ "$CONFIG_COMMITTED" = true ]; then
    echo -e "${BLUE}📦 已提交的仓库：${NC}"
    [ "$SKILLS_COMMITTED" = true ] && echo -e "  ${GREEN}✓${NC} claude-code-skills: 1 个新提交"
    [ "$CONFIG_COMMITTED" = true ] && echo -e "  ${GREEN}✓${NC} claude-code-config: 1 个新提交"

    echo -e "\n${YELLOW}🚀 下一步：使用 GitHub Desktop 推送${NC}"
    echo -e "  1. 打开 GitHub Desktop"
    [ "$SKILLS_COMMITTED" = true ] && echo -e "  2. 选择 ${BLUE}claude-code-skills${NC} 仓库"
    [ "$SKILLS_COMMITTED" = true ] && echo -e "  3. 点击 ${GREEN}\"Push origin\"${NC} 推送提交"
    [ "$CONFIG_COMMITTED" = true ] && echo -e "  4. 选择 ${BLUE}claude-code-config${NC} 仓库"
    [ "$CONFIG_COMMITTED" = true ] && echo -e "  5. 点击 ${GREEN}\"Push origin\"${NC} 推送提交"

    echo -e "\n${BLUE}💡 提示：${NC}如果 GitHub Desktop 中看不到 \"Push origin\" 按钮，"
    echo -e "       请检查是否已经选择了正确的仓库。"
else
    echo -e "${BLUE}ℹ️  没有检测到更改，无需推送。${NC}"
fi

echo ""
