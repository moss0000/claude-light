# ClaudeLight 项目报告

## 一、需求分析

### 1.1 项目背景

在使用 Claude Code 进行 AI 辅助编程时，开发者经常需要等待 Agent 完成长时间的任务（如代码分析、文件修改、测试执行等）。当前缺乏直观的状态指示方式，开发者需要频繁查看终端输出来了解 Agent 的工作进度。

本项目旨在开发一个桌面状态灯设备，通过红绿灯的直观显示，让开发者无需查看屏幕即可了解 Claude Code Agent 的工作状态。

### 1.2 功能需求

#### 核心功能

| 编号 | 功能 | 描述 |
|---|---|---|
| F-01 | 状态指示 | 通过红/黄/绿三色 LED 显示 Agent 工作状态 |
| F-02 | 自动联动 | 与 Claude Code Hooks 自动集成，无需手动操作 |
| F-03 | 多种灯效 | 支持常亮、闪烁、跑马灯等多种视觉效果 |
| F-04 | 超时保护 | 内置自动超时，避免 LED 长时间高亮 |

#### 状态映射

| Agent 状态 | LED 颜色 | 灯效 | 含义 |
|---|---|---|---|
| 正在工作 | 黄色 | 慢闪 | Agent 正在执行任务 |
| 分析中 | 多色 | 跑马灯 | Agent 正在分析需求 |
| 任务完成 | 绿色 | 常亮 | 任务成功完成 |
| 任务失败 | 红色 | 快闪 | 出现错误 |
| 需要确认 | 红黄交替 | 警灯 | 需要用户确认权限 |

### 1.3 非功能需求

| 编号 | 需求 | 描述 |
|---|---|---|
| NF-01 | 低延迟 | 状态切换延迟 < 1秒 |
| NF-02 | 低功耗 | USB 供电，功耗 < 1W |
| NF-03 | 易安装 | 支持 Windows/macOS/Linux，一键安装 |
| NF-04 | 稳定可靠 | BLE 连接稳定，自动重连 |
| NF-05 | 低成本 | 硬件成本 < 50元人民币 |

### 1.4 用户场景

**场景 1：日常开发**
```
开发者发起任务 -> 黄灯慢闪 -> 绿灯常亮（完成）
```

**场景 2：需要权限确认**
```
Agent 需要执行敏感操作 -> 红黄交替警灯 -> 用户确认 -> 继续工作
```

**场景 3：任务失败**
```
Agent 执行出错 -> 红灯快闪 -> 开发者查看错误
```

---

## 二、实施措施

### 2.1 技术选型

#### 主控芯片：ESP32-C3 SuperMini

**选型理由：**
- 内置 BLE 5.0，无需额外模块
- 体积小巧（22.5×18mm），适合桌面设备
- USB-C 接口，方便供电和烧录
- 成本低（约 15-20 元）
- Arduino 生态支持完善

**备选方案对比：**

| 方案 | 优点 | 缺点 | 结论 |
|---|---|---|---|
| ESP32-C3 | BLE 内置、体积小、成本低 | - | ✅ 选定 |
| Arduino Nano + BLE 模块 | 生态成熟 | 需额外模块、体积大 | ❌ |
| Raspberry Pi Pico W | 性能强 | 功耗高、成本高 | ❌ |

#### 通信方式：BLE 蓝牙

**选型理由：**
- 无需 WiFi 网络配置
- 功耗低
- 延迟低（< 100ms）
- 电脑蓝牙普遍支持

**备选方案对比：**

| 方案 | 优点 | 缺点 | 结论 |
|---|---|---|---|
| BLE | 低功耗、无需网络 | 需要电脑有蓝牙 | ✅ 选定 |
| WiFi + HTTP | 传输距离远 | 配置复杂、功耗高 | ❌ |
| USB 串口 | 简单可靠 | 需要线缆连接 | ❌ |

#### LED 方案：三色独立 LED

**选型理由：**
- 成本低
- 电路简单
- 亮度可调（PWM）
- 便于升级为灯环

### 2.2 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                      开发者电脑                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ Claude Code │───▶│ Hook 脚本   │───▶│ BLE 脚本    │ │
│  │   Agent     │    │ (Python)    │    │ (Python)    │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                                             │          │
│                                             │ BLE      │
└─────────────────────────────────────────────┼──────────┘
                                              │
┌─────────────────────────────────────────────┼──────────┐
│                   ESP32-C3                  │          │
│  ┌─────────────┐    ┌─────────────┐    ┌────┴────┐    │
│  │ BLE 模块    │───▶│ 灯效控制    │───▶│ LED 灯  │    │
│  │             │    │ (Arduino)   │    │ 红/黄/绿 │    │
│  └─────────────┘    └─────────────┘    └─────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 2.3 开发计划

| 阶段 | 任务 | 时间 |
|---|---|---|
| 1 | 硬件准备和焊接 | 1天 |
| 2 | 固件开发和测试 | 1天 |
| 3 | Python 脚本开发 | 1天 |
| 4 | Claude Code Hooks 集成 | 1天 |
| 5 | 文档编写 | 1天 |
| 6 | 测试和优化 | 1天 |

---

## 三、具体实现

### 3.1 硬件实现

#### 3.1.1 接线图

```
ESP32-C3 SuperMini
        │
        ├─ 3.3V ──────────▶ 灯板正极 (+)
        │
        ├─ IO2 ──▶ 220Ω ──▶ L1 (绿灯)
        │
        ├─ IO3 ──▶ 220Ω ──▶ L2 (黄灯)
        │
        └─ IO4 ──▶ 220Ω ──▶ L3 (红灯)
```

#### 3.1.2 焊接要点

1. **限流电阻**：每路 LED 串联 220Ω 电阻，保护 ESP32 和 LED
2. **焊接位置**：只焊在金属焊盘上，不要焊在绿色阻焊层
3. **绝缘处理**：焊接完成后用热缩管保护焊点
4. **检查短路**：焊接后用万用表检查是否短路

### 3.2 固件实现

#### 3.2.1 核心代码结构

```cpp
// BLE 配置
const char* BLE_DEVICE_NAME = "ClaudeLight";
#define SERVICE_UUID        "b8b7e001-7a6b-4f4f-9a8b-11c0ffee0001"
#define MODE_CHAR_UUID      "b8b7e002-7a6b-4f4f-9a8b-11c0ffee0001"

// LED 引脚
const int GREEN_PIN = 2;
const int YELLOW_PIN = 3;
const int RED_PIN = 4;
```

#### 3.2.2 灯效实现

**1. 常亮模式**
```cpp
void setOnly(int red, int yellow, int green) {
    writeLed(RED_PIN, constrain(red, 0, RED_MAX));
    writeLed(YELLOW_PIN, constrain(yellow, 0, YELLOW_MAX));
    writeLed(GREEN_PIN, constrain(green, 0, GREEN_MAX));
}
```

**2. 闪烁模式（黄灯慢闪）**
```cpp
void updateBusy() {
    unsigned long t = millis() - modeStart;
    int y = fadeInOutBrightness(t, 80, 500, 120, 500, YELLOW_MAX);
    setOnly(0, y, 0);
}
```

**3. 跑马灯模式**
```cpp
void updateThinking() {
    unsigned long t = millis() - modeStart;
    const unsigned long period = 1050;
    unsigned long x = t % period;
    
    // 绿 -> 黄 -> 红 循环
    if (x < 350) {
        // 绿灯渐暗，黄灯渐亮
    } else if (x < 700) {
        // 黄灯渐暗，红灯渐亮
    } else {
        // 红灯渐暗，绿灯渐亮
    }
}
```

**4. 警灯模式（红黄交替）**
```cpp
void updateAlarm() {
    unsigned long t = millis() - modeStart;
    const unsigned long phaseMs = 260;
    int phase = (t / phaseMs) % 2;
    
    if (phase == 0) {
        setOnly(brightness, 0, 0);  // 红灯
    } else {
        setOnly(0, brightness, 0);  // 黄灯
    }
}
```

#### 3.2.3 BLE 通信

**GATT 服务配置**
```cpp
BLEService* pService = pServer->createService(SERVICE_UUID);

pModeCharacteristic = pService->createCharacteristic(
    MODE_CHAR_UUID,
    BLECharacteristic::PROPERTY_READ |
    BLECharacteristic::PROPERTY_WRITE |
    BLECharacteristic::PROPERTY_NOTIFY
);
```

**接收指令处理**
```cpp
class ModeCharacteristicCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic* pCharacteristic) {
        String value = pCharacteristic->getValue();
        value.trim();
        setMode(value);  // 设置灯效模式
    }
};
```

#### 3.2.4 自动超时

```cpp
void autoTimeoutCheck() {
    unsigned long elapsed = millis() - modeStart;
    
    if (currentMode == "traffic") {
        if (elapsed >= TRAFFIC_MODE_TIMEOUT_MS) {  // 10分钟
            setMode("off");
        }
    } else {
        if (elapsed >= NORMAL_MODE_TIMEOUT_MS) {  // 5分钟
            setMode("traffic");
        }
    }
}
```

### 3.3 Python 脚本实现

#### 3.3.1 BLE 控制脚本

**设备扫描**
```python
async def find_device():
    devices = await BleakScanner.discover(timeout=5.0)
    for device in devices:
        if device.name and "ClaudeLight" in device.name:
            return device
    return None
```

**发送指令**
```python
async def send_mode(mode: str):
    device = await find_device()
    if not device:
        return False
    
    async with BleakClient(device) as client:
        await client.write_gatt_char(MODE_CHAR_UUID, mode.encode())
        return True
```

#### 3.3.2 Hook 集成脚本

**事件映射**
```python
EVENT_MODE_MAP = {
    "PreToolUse": "busy",      # 工具调用前
    "PostToolUse": "success",  # 工具调用后
    "Notification": "alarm",   # 需要确认
    "Stop": "success",         # Agent 停止
}
```

**防抖处理**
```python
def should_process_event(event_type: str) -> bool:
    now = datetime.now()
    last_time = last_event_time.get(event_type)
    
    if last_time:
        elapsed = (now - last_time).total_seconds() * 1000
        if elapsed < DEBOUNCE_MS:  # 500ms
            return False
    
    last_event_time[event_type] = now
    return True
```

### 3.4 Claude Code Hooks 配置

#### 3.4.1 settings.json 配置

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/claude-light/claude_light_hook.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/claude-light/claude_light_hook.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/claude-light/claude_light_hook.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/claude-light/claude_light_hook.py"
          }
        ]
      }
    ]
  }
}
```

#### 3.4.2 事件处理流程

```
Claude Code 事件
      │
      ▼
┌─────────────┐
│ Hook 脚本   │
│ 接收 JSON   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 防抖检查    │ 500ms 内相同事件只处理一次
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 事件映射    │ 确定灯效模式
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ BLE 发送    │ 发送指令到 ESP32
└─────────────┘
```

---

## 四、测试方案

### 4.1 单元测试

| 测试项 | 测试方法 | 预期结果 |
|---|---|---|
| LED 控制 | 手动设置各引脚高/低电平 | LED 正确亮/灭 |
| BLE 广播 | 使用手机 BLE 扫描 | 能发现 ClaudeLight 设备 |
| BLE 读写 | 使用 BLE 调试工具 | 能读写模式值 |
| 灯效切换 | 发送不同模式指令 | 灯效正确切换 |

### 4.2 集成测试

| 测试项 | 测试方法 | 预期结果 |
|---|---|---|
| Claude Code 联动 | 执行一个任务 | 灯效随状态变化 |
| 权限确认 | 触发需要确认的操作 | 红黄交替警灯 |
| 任务完成 | 等待任务完成 | 绿灯常亮 |
| 任务失败 | 触发错误 | 红灯快闪 |

### 4.3 压力测试

| 测试项 | 测试方法 | 预期结果 |
|---|---|---|
| 长时间运行 | 连续运行 24 小时 | 无异常 |
| 快速切换 | 快速连续发送指令 | 不丢失指令 |
| 断连重连 | 蓝牙断开后重连 | 自动重连成功 |

---

## 五、风险评估

| 风险 | 影响 | 概率 | 缓解措施 |
|---|---|---|---|
| BLE 连接不稳定 | 灯效不响应 | 低 | 实现自动重连机制 |
| 电脑无蓝牙 | 无法使用 | 中 | 提供 USB 蓝牙适配器方案 |
| 焊接不良 | LED 不亮 | 中 | 提供详细焊接指南 |
| Claude Code Hooks 变更 | 集成失效 | 低 | 关注官方文档更新 |

---

## 六、成本分析

### 6.1 硬件成本

| 物料 | 单价 | 数量 | 小计 |
|---|---|---:|---:|
| ESP32-C3 SuperMini | ¥15 | 1 | ¥15 |
| 红绿灯挂件 | ¥10 | 1 | ¥10 |
| 220Ω 电阻 | ¥0.1 | 3 | ¥0.3 |
| 导线 | ¥2 | 1 | ¥2 |
| USB-C 线 | ¥5 | 1 | ¥5 |
| 热缩管 | ¥1 | 1 | ¥1 |
| **合计** | | | **¥33.3** |

### 6.2 开发成本

- 开发时间：约 6 天
- 测试时间：约 2 天
- 文档编写：约 1 天

---

## 七、总结

ClaudeLight 项目通过简单的硬件改装和软件集成，为 Claude Code 开发者提供了一个直观的状态指示方案。项目具有以下特点：

1. **低成本**：硬件成本仅需 33 元
2. **易安装**：一键安装脚本，支持多平台
3. **自动化**：与 Claude Code Hooks 无缝集成
4. **可扩展**：支持升级为 RGB 灯环或 OLED 屏幕

该项目可以显著提升开发者的工作效率，减少不必要的屏幕查看，让 AI 辅助编程更加流畅。
