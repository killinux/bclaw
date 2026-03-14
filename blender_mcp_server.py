#!/usr/bin/env python3
"""Blender MCP Server - 使用官方 MCP SDK"""

import socket
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl
import asyncio


# 创建 MCP 服务器
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
    """列出可用的工具"""
    return [
        Tool(
            name="blender_status",
            description="检查 Blender MCP 状态",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="blender_scene",
            description="获取 Blender 场景信息",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="blender_objects",
            description="获取场景中的所有对象",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="blender_exec",
            description="执行 Blender Python 代码",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "要执行的 Blender Python 代码"
                    }
                },
                "required": ["code"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """执行工具调用"""
    try:
        if name == "blender_status":
            result = send_to_blender("get_polyhaven_status")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "blender_scene":
            result = send_to_blender("get_scene_info")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "blender_objects":
            code = "import json; objects = [{'name': obj.name, 'type': obj.type} for obj in bpy.data.objects]; print(json.dumps(objects))"
            result = send_to_blender("execute_code", params={"code": code})
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "blender_exec":
            code = arguments.get("code", "")
            result = send_to_blender("execute_code", params={"code": code})
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        else:
            return [TextContent(type="text", text=f"未知工具: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"错误: {str(e)}")]


async def main():
    """主函数"""
    async with stdio_server() as (read, write):
        await app.run(
            read,
            write,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
