#!/bin/bash
# ClaudeLight 安装脚本 (macOS/Linux)

set -e

echo "=== ClaudeLight 安装脚本 ==="
echo ""

# 创建目录
INSTALL_DIR="$HOME/.claude/claude-light"
echo "创建安装目录: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# 复制文件
echo "复制文件..."
cp "$(dirname "$0")/claude_light_ble.py" "$INSTALL_DIR/"
cp "$(dirname "$0")/claude_light_hook.py" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/claude_light_ble.py"
chmod +x "$INSTALL_DIR/claude_light_hook.py"

# 检查 Python
echo ""
echo "检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "错误: 未找到 Python，请先安装 Python 3.x"
    exit 1
fi

PYTHON_VERSION=$($PYTHON --version 2>&1)
echo "Python: $PYTHON_VERSION"

# 安装依赖
echo ""
echo "安装 Python 依赖..."
$PYTHON -m pip install --user bleak

# 配置 Claude Code hooks
echo ""
echo "配置 Claude Code hooks..."
SETTINGS_FILE="$HOME/.claude/settings.json"

if [ -f "$SETTINGS_FILE" ]; then
    echo "警告: settings.json 已存在"
    echo "请手动合并以下配置到 $SETTINGS_FILE"
    echo ""
    cat "$(dirname "$0")/settings.json.snippet"
else
    cp "$(dirname "$0")/settings.json.snippet" "$SETTINGS_FILE"
    echo "已创建 settings.json"
fi

# 测试
echo ""
echo "=== 安装完成 ==="
echo ""
echo "请先将固件烧录到 ESP32-C3，然后运行以下命令测试:"
echo "  $PYTHON $INSTALL_DIR/claude_light_ble.py green"
echo "  $PYTHON $INSTALL_DIR/claude_light_ble.py thinking"
echo "  $PYTHON $INSTALL_DIR/claude_light_ble.py success"
echo ""
