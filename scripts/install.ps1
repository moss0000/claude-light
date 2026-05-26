# ClaudeLight 安装脚本 (Windows PowerShell)

Write-Host "=== ClaudeLight 安装脚本 ===" -ForegroundColor Cyan
Write-Host ""

# 创建目录
$installDir = "$env:USERPROFILE\.claude\claude-light"
Write-Host "创建安装目录: $installDir"
New-Item -ItemType Directory -Force -Path $installDir | Out-Null

# 复制文件
Write-Host "复制文件..."
Copy-Item "$PSScriptRoot\claude_light_ble.py" "$installDir\" -Force
Copy-Item "$PSScriptRoot\claude_light_hook.py" "$installDir\" -Force

# 检查 Python
Write-Host ""
Write-Host "检查 Python..."
try {
    $pythonVersion = py --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: 未找到 Python，请先安装 Python 3.x" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host ""
Write-Host "安装 Python 依赖..."
py -m pip install --user bleak

# 配置 Claude Code hooks
Write-Host ""
Write-Host "配置 Claude Code hooks..."
$settingsFile = "$env:USERPROFILE\.claude\settings.json"

if (Test-Path $settingsFile) {
    Write-Host "警告: settings.json 已存在" -ForegroundColor Yellow
    Write-Host "请手动合并以下配置到 $settingsFile" -ForegroundColor Yellow
    Write-Host ""
    Get-Content "$PSScriptRoot\settings.json.snippet"
} else {
    Copy-Item "$PSScriptRoot\settings.json.snippet" $settingsFile -Force
    Write-Host "已创建 settings.json" -ForegroundColor Green
}

# 测试
Write-Host ""
Write-Host "=== 安装完成 ===" -ForegroundColor Green
Write-Host ""
Write-Host "请先将固件烧录到 ESP32-C3，然后运行以下命令测试:" -ForegroundColor Cyan
Write-Host "  py $installDir\claude_light_ble.py green"
Write-Host "  py $installDir\claude_light_ble.py thinking"
Write-Host "  py $installDir\claude_light_ble.py success"
Write-Host ""
