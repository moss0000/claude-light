#!/usr/bin/env python3
"""
ClaudeLight Hook 集成脚本
用于 Claude Code 的 hooks 系统，自动将 Agent 状态映射到灯效
"""

import asyncio
import json
import sys
import os
import logging
from datetime import datetime
from pathlib import Path

try:
    from bleak import BleakClient, BleakScanner
except ImportError:
    sys.exit(0)  # 静默退出，不影响 Claude Code 正常运行

# BLE 配置
DEVICE_NAME = "ClaudeLight"
SERVICE_UUID = "b8b7e001-7a6b-4f4f-9a8b-11c0ffee0001"
MODE_CHAR_UUID = "b8b7e002-7a6b-4f4f-9a8b-11c0ffee0001"

# 日志文件
LOG_DIR = Path.home() / ".claude" / "claude-light"
LOG_FILE = LOG_DIR / "claude_light.log"

# 状态映射
# Claude Code Hook 事件 -> 灯效模式
EVENT_MODE_MAP = {
    # Agent 开始工作 - 黄灯慢闪
    "PreToolUse": "busy",
    # Agent 完成工具调用 - 绿灯常亮
    "PostToolUse": "success",
    # 需要用户确认权限 - 红灯快闪
    "Notification": "alarm",
    # Agent 停止工作 - 绿灯常亮
    "Stop": "success",
    # 子 Agent 停止 - 绿灯常亮
    "SubagentStop": "success",
}

# 特殊通知类型映射
NOTIFICATION_MODE_MAP = {
    "permission": "alarm",  # 需要权限确认
    "error": "error",  # 错误
    "warning": "yellow",  # 警告
    "info": "thinking",  # 信息
}

# 防抖配置
DEBOUNCE_MS = 500  # 500ms 内相同事件只处理一次
last_event_time = {}
last_mode = None


def setup_logging():
    """设置日志"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


async def send_mode(mode: str):
    """发送模式到 ClaudeLight"""
    global last_mode

    # 防抖：相同模式不重复发送
    if mode == last_mode:
        return True

    try:
        devices = await BleakScanner.discover(timeout=3.0)
        device = None

        for d in devices:
            if d.name and DEVICE_NAME in d.name:
                device = d
                break

        if not device:
            return False

        async with BleakClient(device) as client:
            await client.write_gatt_char(MODE_CHAR_UUID, mode.encode())
            last_mode = mode
            logger.info(f"已发送模式: {mode}")
            return True

    except Exception as e:
        logger.debug(f"BLE 发送失败: {e}")
        return False


def should_process_event(event_type: str) -> bool:
    """防抖检查"""
    now = datetime.now()
    last_time = last_event_time.get(event_type)

    if last_time:
        elapsed = (now - last_time).total_seconds() * 1000
        if elapsed < DEBOUNCE_MS:
            return False

    last_event_time[event_type] = now
    return True


def determine_mode(hook_data: dict) -> str:
    """根据 hook 数据确定灯效模式"""
    event_type = hook_data.get("event_type", "")

    # 通知事件特殊处理
    if event_type == "Notification":
        notification = hook_data.get("notification", {})
        notif_type = notification.get("type", "")
        return NOTIFICATION_MODE_MAP.get(notif_type, "alarm")

    # 默认映射
    return EVENT_MODE_MAP.get(event_type, "thinking")


def main():
    """主函数 - 从 stdin 读取 Claude Code hook 数据"""
    try:
        # 从 stdin 读取 JSON 数据
        input_data = sys.stdin.read()

        if not input_data.strip():
            sys.exit(0)

        # 解析 JSON
        try:
            hook_data = json.loads(input_data)
        except json.JSONDecodeError:
            logger.error(f"JSON 解析失败: {input_data[:100]}")
            sys.exit(0)

        event_type = hook_data.get("event_type", "unknown")
        logger.info(f"收到事件: {event_type}")

        # 防抖检查
        if not should_process_event(event_type):
            logger.debug(f"事件被防抖过滤: {event_type}")
            sys.exit(0)

        # 确定模式
        mode = determine_mode(hook_data)
        logger.info(f"映射模式: {mode}")

        # 发送 BLE 指令（异步）
        result = asyncio.run(send_mode(mode))

        if result:
            logger.info("灯效更新成功")
        else:
            logger.warning("灯效更新失败")

    except Exception as e:
        logger.error(f"Hook 处理异常: {e}")

    sys.exit(0)


if __name__ == "__main__":
    main()
