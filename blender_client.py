#!/usr/bin/env python3
"""Blender MCP 客户端 - 通过 uv 运行"""

import socket
import json
import sys


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


def main():
    if len(sys.argv) < 2:
        print("用法: python blender_client.py <command> [args...]")
        print("命令:")
        print("  status              - 检查 Blender MCP 状态")
        print("  scene               - 获取场景信息")
        print("  objects             - 获取场景中的对象")
        print("  exec <code>        - 执行 Blender Python 代码")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    try:
        if cmd == "status":
            result = send_to_blender("get_polyhaven_status")
            print(json.dumps(result, indent=2))
        
        elif cmd == "scene":
            result = send_to_blender("get_scene_info")
            print(json.dumps(result, indent=2))
        
        elif cmd == "objects":
            # 获取场景中所有对象
            code = "import json; objects = [{'name': obj.name, 'type': obj.type} for obj in bpy.data.objects]; print(json.dumps(objects))"
            result = send_to_blender("execute_code", params={"code": code})
            print(json.dumps(result, indent=2))
        
        elif cmd == "exec":
            if len(sys.argv) < 3:
                print("错误: 请提供要执行的代码")
                sys.exit(1)
            code = sys.argv[2]
            result = send_to_blender("execute_code", params={"code": code})
            print(json.dumps(result, indent=2))
        
        else:
            print(f"未知命令: {cmd}")
            sys.exit(1)
    
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
