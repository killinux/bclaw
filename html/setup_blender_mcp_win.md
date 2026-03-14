# 🦞 OpenClaw 连接 Blender MCP 指南 (Windows)

> **摘要：** 本文档介绍如何在 Windows 上让 OpenClaw 通过 uv + mcporter 连接 Blender MCP，实现用 AI 控制 Blender。

---

## 🔄 三种连接方案

### 方案一：直接 Python Socket（最简单）
```
OpenClaw → blender-tool.py (Python socket) → Blender MCP
```

### 方案二：uv + mcporter（推荐）
```
OpenClaw → mcporter → uv run → blender_mcp_server.py → Blender MCP
```

### 方案三：Claude Code + uv
```
Claude Code → uv run → blender_client.py → Blender MCP
```

---

## 🔄 方案一架构图（直接 Python Socket）

```
┌─────────────────────────────────────────────────────────────────────┐
│                        OpenClaw (AI 助手)                           │
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  blender-tool.py (自定义 Python 脚本)                        │  │
│   │  └── 通过 socket 发送 JSON 命令到 Blender                    │  │
│   └─────────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ socket
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
4. **重要：** 将端口改为 `8765`

---

## 📝 方案一：直接 Python Socket（最简单）

### 核心脚本：blender-tool.py

文件位置：`C:\Users\haoni\blender-tool.py`

```python
import socket
import json
import sys

def send_to_blender(msg_type, **kwargs):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8765))

    msg = {"type": msg_type, **kwargs}
    s.send(json.dumps(msg).encode())
    s.settimeout(30)

    result = s.recv(65536).decode()
    s.close()
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "status":
            print(send_to_blender("get_polyhaven_status"))
        elif cmd == "scene":
            print(send_to_blender("get_scene_info"))
    else:
        print(json.dumps({"status": "error", "message": "No command provided"}))
```

### 执行代码脚本

```python
import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8765))

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

### 测试

```bash
# 检查状态
D:\openclaw\python\python.exe C:\Users\haoni\blender-tool.py status

# 执行代码
D:\openclaw\python\python.exe C:\Users\haoni\create-cube.py
```

---

## 🚀 方案二：uv + mcporter（推荐）

### 2.1 安装 uv

```bash
# 使用 OpenClaw 自带的 uv
uv --version
```

### 2.2 安装 mcporter

```bash
npm install -g mcporter
```

### 2.3 创建项目结构

```bash
mkdir E:\mywork\bclaw
cd E:\mywork\bclaw
```

### 2.4 创建 pyproject.toml

```toml
[project]
name = "blender-mcp-client"
version = "0.1.0"
description = "Blender MCP Client via uv"
requires-python = ">=3.10"
dependencies = []

[dependency-groups]
dev = []
```

### 2.5 安装 MCP 依赖

```bash
cd E:\mywork\bclaw
uv add mcp
```

### 2.6 创建 MCP Server：blender_mcp_server.py

```python
#!/usr/bin/env python3
"""Blender MCP Server - 使用官方 MCP SDK"""

import socket
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio


app = Server("blender-mcp")


def send_to_blender(msg_type: str, **kwargs) -> dict:
    """发送命令到 Blender MCP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8765))
    
    msg = {"type": msg_type, **kwargs}
    s.send(json.dumps(msg).encode())
    s.settimeout(30)
    
    result = s.recv(65536).decode()
    s.close()
    return json.loads(result)


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="blender_status",
            description="检查 Blender MCP 状态",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="blender_scene",
            description="获取 Blender 场景信息",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="blender_objects",
            description="获取场景中的所有对象",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="blender_exec",
            description="执行 Blender Python 代码",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "要执行的 Blender Python 代码"}
                },
                "required": ["code"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "blender_status":
            result = send_to_blender("get_polyhaven_status")
        elif name == "blender_scene":
            result = send_to_blender("get_scene_info")
        elif name == "blender_objects":
            code = "import json; objects = [{'name': obj.name, 'type': obj.type} for obj in bpy.data.objects]; print(json.dumps(objects))"
            result = send_to_blender("execute_code", params={"code": code})
        elif name == "blender_exec":
            code = arguments.get("code", "")
            result = send_to_blender("execute_code", params={"code": code})
        else:
            return [TextContent(type="text", text=f"未知工具: {name}")]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"错误: {str(e)}")]


async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
```

### 2.7 配置 mcporter

```bash
mcporter config add blender --command "uv run --directory E:\\mywork\\bclaw python blender_mcp_server.py"
```

### 2.8 测试

```bash
# 列出工具
mcporter list blender --schema

# 调用工具
mcporter call blender.blender_status
mcporter call blender.blender_exec code="import bpy; bpy.ops.mesh.primitive_cube_add(size=1)"
```

---

## 💻 方案三：Claude Code + uv

### 3.1 安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 3.2 登录 Claude Code

```bash
claude auth login
```

### 3.3 创建客户端脚本：blender_client.py

```python
#!/usr/bin/env python3
"""Blender MCP 客户端 - 通过 uv 运行"""

import socket
import json
import sys


def send_to_blender(msg_type: str, **kwargs) -> dict:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8765))
    
    msg = {"type": msg_type, **kwargs}
    s.send(json.dumps(msg).encode())
    s.settimeout(30)
    
    result = s.recv(65536).decode()
    s.close()
    return json.loads(result)


def main():
    if len(sys.argv) < 2:
        print("用法: python blender_client.py <command> [args...]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    try:
        if cmd == "status":
            result = send_to_blender("get_polyhaven_status")
        elif cmd == "scene":
            result = send_to_blender("get_scene_info")
        elif cmd == "objects":
            code = "import json; objects = [{'name': obj.name, 'type': obj.type} for obj in bpy.data.objects]; print(json.dumps(objects))"
            result = send_to_blender("execute_code", params={"code": code})
        elif cmd == "exec":
            if len(sys.argv) < 3:
                print("错误: 请提供要执行的代码")
                sys.exit(1)
            code = sys.argv[2]
            result = send_to_blender("execute_code", params={"code": code})
        else:
            print(f"未知命令: {cmd}")
            sys.exit(1)
        
        print(json.dumps(result, indent=2))
    
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 3.4 测试

```bash
cd E:\mywork\bclaw

# 检查状态
uv run python blender_client.py status

# 获取对象列表
uv run python blender_client.py objects

# 执行代码
uv run python blender_client.py exec "import bpy; bpy.ops.mesh.primitive_cube_add(size=1)"
```

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

## ⚡ 快速命令参考

```bash
# 检查 Blender MCP 端口
Get-NetTCPConnection -LocalPort 8765

# 方案一：直接运行
D:\openclaw\python\python.exe C:\Users\haoni\blender-tool.py status

# 方案二：uv + mcporter
mcporter call blender.blender_status

# 方案三：uv 客户端
cd E:\mywork\bclaw
uv run python blender_client.py status
```

---

## 📚 相关文件位置

| 文件 | 路径 |
|------|------|
| MCP Server | `E:\mywork\bclaw\blender_mcp_server.py` |
| 客户端脚本 | `E:\mywork\bclaw\blender_client.py` |
| 项目配置 | `E:\mywork\bclaw\pyproject.toml` |
| blender-tool.py | `C:\Users\haoni\blender-tool.py` |
| blender-mcp 源码 | `E:\Downloads\blender-mcp-main` |

---

## 🔧 常见问题

### Q1: 连接失败 "Connection refused"

确保 Blender 已启动且 BlenderMCP 插件已启用，端口 8765 正在监听。

### Q2: "Unknown command type"

检查命令格式，确保使用正确的 JSON 结构。

### Q3: uv 找不到命令

确保在正确的目录下运行，或使用绝对路径。

---

*由 OpenClaw AI 助手生成 | 2026.03.14*
