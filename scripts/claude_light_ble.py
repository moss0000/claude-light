#!/usr/bin/env python3
"""
ClaudeLight BLE 控制脚本
用于向 ESP32-C3 发送 BLE 指令控制灯效
"""

import asyncio
import sys
import logging
from datetime import datetime

try:
    from bleak import BleakClient, BleakScanner
except ImportError:
    print("请先安装 bleak: pip install bleak")
    sys.exit(1)

# BLE 配置
DEVICE_NAME = "ClaudeLight"
SERVICE_UUID = "b8b7e001-7a6b-4f4f-9a8b-11c0ffee0001"
MODE_CHAR_UUID = "b8b7e002-7a6b-4f4f-9a8b-11c0ffee0001"

# 有效模式列表
VALID_MODES = [
    "demo", "thinking", "ai", "busy", "success",
    "error", "alarm", "traffic", "off",
    "red", "yellow", "green"
]

# 日志配置
LOG_FILE = "claude_light_ble.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def find_device():
    """扫描并查找 ClaudeLight 设备"""
    logger.info(f"正在扫描 BLE 设备: {DEVICE_NAME}...")
    devices = await BleakScanner.discover(timeout=5.0)

    for device in devices:
        if device.name and DEVICE_NAME in device.name:
            logger.info(f"找到设备: {device.name} ({device.address})")
            return device

    logger.error(f"未找到 {DEVICE_NAME} 设备")
    return None


async def send_mode(mode: str):
    """发送模式指令到 ClaudeLight"""
    if mode not in VALID_MODES:
        logger.error(f"无效模式: {mode}")
        logger.info(f"有效模式: {', '.join(VALID_MODES)}")
        return False

    device = await find_device()
    if not device:
        return False

    try:
        async with BleakClient(device) as client:
            logger.info(f"已连接到 {device.name}")

            # 写入模式
            await client.write_gatt_char(MODE_CHAR_UUID, mode.encode())
            logger.info(f"已发送模式: {mode}")

            # 等待一下确保写入完成
            await asyncio.sleep(0.1)

            logger.info("指令发送成功")
            return True

    except Exception as e:
        logger.error(f"BLE 通信失败: {e}")
        return False


async def read_mode():
    """读取当前模式"""
    device = await find_device()
    if not device:
        return None

    try:
        async with BleakClient(device) as client:
            value = await client.read_gatt_char(MODE_CHAR_UUID)
            mode = value.decode("utf-8").strip()
            logger.info(f"当前模式: {mode}")
            return mode

    except Exception as e:
        logger.error(f"读取失败: {e}")
        return None


def print_usage():
    """打印使用说明"""
    print("ClaudeLight BLE 控制脚本")
    print()
    print("用法:")
    print(f"  python {sys.argv[0]} <mode>")
    print(f"  python {sys.argv[0]} --read")
    print()
    print("可用模式:")
    for mode in VALID_MODES:
        print(f"  - {mode}")
    print()
    print("示例:")
    print(f"  python {sys.argv[0]} thinking")
    print(f"  python {sys.argv[0]} success")
    print(f"  python {sys.argv[0]} --read")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    arg = sys.argv[1].lower()

    if arg in ("--help", "-h"):
        print_usage()
        sys.exit(0)

    if arg == "--read":
        result = asyncio.run(read_mode())
        if result is None:
            sys.exit(1)
    else:
        result = asyncio.run(send_mode(arg))
        if not result:
            sys.exit(1)


if __name__ == "__main__":
    main()
