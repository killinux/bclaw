# 🦞 OpenClaw 连接 Blender MCP 指南 (Windows)

> **摘要：** 本文档介绍如何在 Windows 上让 OpenClaw 通过自定义 Python 脚本连接 Blender MCP，实现用 AI 控制 Blender。

---

## 🔄 连接架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                        OpenClaw (AI 助手)                           │
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  mcporter (MCP 客户端) 或 直接调用 Python 脚本               │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  blender-tool.py (自定义 Python 脚本)                        │  │
│   │  └── 通过 socket 发送 JSON 命令到 Blender                    │  │
│   └─────────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ stdio / socket
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   blender-tool.py (Python 脚本)                      │
│   └── 通过 TCP socket 连接到 127.0.0.1:8765                         │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ TCP:8765
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 Blender (运行中)                                     │
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  BlenderMCP 插件 (addon.py)                                  │  │
│   │  └── 监听 8765 端口，执行 Python 代码操作 Blender (bpy)      │  │
│   └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ 重要前提

> **为什么不用官方 MCP 包？**
>
> 官方 `@iflow-mcp/pranav-deshmukh-blender-mcp` npm 包默认连接端口 8765，但存在 stdio 通信不稳定的问题。
>
> **解决方案：** 直接用 Python socket 编写自定义脚本，简单可靠。

---

## 📦 步骤一：Blender 端配置

### 1.1 下载 BlenderMCP 插件

从 GitHub 下载 BlenderMCP 插件：

```
https://github.com/pranav-deshmukh/blender-mcp
```

或直接从 npm 安装（可选）：

```bash
npm install -g @iflow-mcp/pranav-deshmukh-blender-mcp
```

### 1.2 在 Blender 中安装插件

1. 打开 Blender
2. Edit → Preferences → Add-ons
3. 点击右上角 "Install from file"
4. 选择下载的 `blender-mcp-main.zip` 文件
5. 搜索 "blender-mcp" 并启用插件

### 1.3 启用 BlenderMCP 并设置端口

1. 在 Blender 界面按 `N` 键打开 Sidebar
2. 找到 **BlenderMCP** 面板
3. 确保 **Server** 状态为 Running
4. **重要：** 将端口改为 `8765`（与官方 npm 包默认端口一致）

> **注意：** 官方 npm 包默认连接 8765，所以需要在 Blender 中将端口改为 8765。

---

## 🐍 步骤二：安装 Python 和依赖

### 2.1 安装 Python（如果未安装）

本方案使用 OpenClaw 自带的 Python：

```
D:\openclaw\python\python.exe
```

---

## 📝 步骤三：创建连接脚本

### 3.1 核心脚本：blender-tool.py

文件位置：`C:\Users\haoni\blender-tool.py`

```python
import socket
import json
import sys

def send_to_blender(msg_type, **kwargs):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8765))  # 连接 Blender MCP 端口

    msg = {"type": msg_type, **kwargs}  # 构建 JSON 消息
    s.send(json.dumps(msg).encode())    # 发送
    s.settimeout(30)

    result = s.recv(65536).decode()     # 接收结果
    s.close()
    return result

# 从命令行参数读取命令
if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if cmd == "status":
        print(send_to_blender("get_polyhaven_status"))
    elif cmd == "scene":
        print(send_to_blender("fetch-scene"))
    else:
        print(json.dumps({"status": "error", "message": f"Unknown command: {cmd}"}))
else:
    print(json.dumps({"status": "error", "message": "No command provided"}))
```

### 3.2 执行代码脚本：create-cube.py

用于向 Blender 发送 Python 代码命令

```python
import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8765))

# 发送 execute_code 命令
msg = {
    "type": "execute_code",
    "params": {
        "code": "import bpy; bpy.ops.mesh.primitive_cube_add(size=2)"
    }
}
s.send(json.dumps(msg).encode())
s.settimeout(10)

print(s.recv(8192).decode())
s.close()
```

---

## 🧪 步骤四：测试连接

### 4.1 检查 Blender MCP 端口

```powershell
# 在 PowerShell 中检查端口是否在监听
Get-NetTCPConnection -LocalPort 8765
```

### 4.2 测试连接

```bash
# 检查状态
D:\openclaw\python\python.exe C:\Users\haoni\blender-tool.py status

# 执行代码创建立方体
D:\openclaw\python\python.exe C:\Users\haoni\create-cube.py
```

> **成功响应示例：**
> ```json
> {"status": "success", "result": {"executed": true, "result": ""}}
> ```

---

## 🔌 Blender MCP 协议格式

### JSON 命令格式

```json
{
    "type": "execute_code",
    "params": {
        "code": "import bpy; bpy.ops.mesh.primitive_cube_add(size=2)"
    }
}
```

### 可用命令列表

| 命令 | 说明 |
|------|------|
| `get_scene_info` | 获取场景信息 |
| `get_object_info` | 获取对象信息 |
| `get_viewport_screenshot` | 获取视口截图 |
| `execute_code` | 执行任意 Blender Python 代码 |
| `get_polyhaven_status` | PolyHaven 集成状态 |
| `get_sketchfab_status` | Sketchfab 集成状态 |
| `get_hunyuan3d_status` | Hunyuan3D 状态 |

---

## 🐙 步骤五：配置 GitHub（可选）

### 5.1 检查 SSH 密钥

```bash
dir C:\Users\haoni\.ssh\
```

### 5.2 配置 Git

```bash
# 设置用户名
git config --global user.name "your-username"

# 设置邮箱
git config --global user.email "your-email@example.com"

# 添加安全目录（如果需要）
git config --global --add safe.directory E:/mywork/bclaw
```

### 5.3 测试 GitHub 连接

```bash
ssh -T git@github.com
```

> **成功响应：** `Hi username! You've successfully authenticated...`

---

## 📚 相关文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| blender-tool.py | `C:\Users\haoni\blender-tool.py` | 核心连接脚本 |
| create-cube.py | `C:\Users\haoni\create-cube.py` | 测试脚本 - 创建立方体 |
| blender-mcp 源码 | `E:\Downloads\blender-mcp-main` | Blender MCP 插件源码 |
| OpenClaw 配置 | `C:\Users\haoni\.openclaw\openclaw.json` | OpenClaw 主配置 |

---

## ⚡ 快速命令参考

```bash
# 测试 Blender 连接
D:\openclaw\python\python.exe -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 8765)); print('Connected')"

# 检查端口状态
Get-NetTCPConnection -LocalPort 8765

# 执行 Blender 代码
D:\openclaw\python\python.exe C:\Users\haoni\create-cube.py
```

---

## 🔧 常见问题

### Q1: 连接失败 "Connection refused"

确保 Blender 已启动且 BlenderMCP 插件已启用，端口 8765 正在监听。

### Q2: "Unknown command type"

检查命令格式，确保使用正确的 JSON 结构：
```json
{"type": "execute_code", "params": {"code": "..."}}
```

### Q3: 端口被占用

可以使用其他端口，但需要同时修改 BlenderMCP 插件设置和脚本中的端口号。

---

*由 OpenClaw AI 助手生成 | 2026.03.14*
