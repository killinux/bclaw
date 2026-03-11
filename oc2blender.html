<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>OpenClaw 通过 MCP 调用本地 Blender 示例（生成球体）</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif; line-height: 1.6; padding: 24px; max-width: 900px; margin: 0 auto; }
    code, pre { font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
    pre { background: #f5f5f7; padding: 12px 16px; border-radius: 6px; overflow-x: auto; }
    h1, h2, h3 { line-height: 1.3; }
    h1 { margin-top: 0; }
    hr { margin: 32px 0; border: none; border-top: 1px solid #ddd; }
    .step { margin-bottom: 24px; }
    .note { background: #fffbe6; border-left: 4px solid #f5c518; padding: 10px 12px; border-radius: 4px; }
    .ok { color: #1a7f37; }
    .warn { color: #b54708; }
  </style>
</head>
<body>
  <h1>OpenClaw 通过 MCP 调用本地 Blender 示例：生成一个球体</h1>

  <p>本文档记录了在 macOS 上，让 <strong>OpenClaw</strong> 通过 <strong>MCP（Model Context Protocol）</strong> 调用本地 <strong>Blender 4.2</strong>，并在场景中创建一个 <strong>球体</strong> 的完整过程。</p>

  <p>环境假设：</p>
  <ul>
    <li>系统：macOS</li>
    <li>Blender 路径：<code>/Applications/Blender4.2.app/Contents/MacOS/Blender</code></li>
    <li>OpenClaw 已安装并运行在当前用户下</li>
    <li>命令均在当前用户的终端下执行</li>
  </ul>

  <hr />

  <h2>一、整体架构说明</h2>

  <p>完整链路如下：</p>

  <pre><code>你（在 OpenClaw 里发指令）
      ↓
OpenClaw / mcporter
      ↓  （MCP 协议）
blender-mcp MCP Server（Python，uvx 启动）
      ↓  （TCP socket，本机 localhost:9876）
Blender 插件 addon.py（在 Blender 进程内部）
      ↓
Blender Python API（bpy）真正创建对象（球体 / 立方体等）
</code></pre>

  <p>本文重点是：</p>
  <ol>
    <li>安装/准备工具：<code>uv</code>、<code>blender-mcp</code></li>
    <li>在 Blender 中安装 <code>addon.py</code></li>
    <li>配置 <code>mcporter</code> 的 MCP Server</li>
    <li>通过 MCP 调用 Blender，在场景中生成一个球体</li>
  </ol>

  <hr />

  <h2>二、前置安装</h2>

  <div class="step">
    <h3>1. 安装 uv（如未安装）</h3>
    <p>OpenClaw 的环境中已经安装了 uv（示例环境里是这样的），如果本机没有，请在终端执行：</p>
    <pre><code>brew install uv</code></pre>
    <p>安装完成后可验证：</p>
    <pre><code>uv --version</code></pre>
  </div>

  <div class="step">
    <h3>2. 安装 / 准备 blender-mcp（MCP Server）</h3>
    <p><code>blender-mcp</code> 是一个 Python 实现的 MCP Server，用于连接 Blender。</p>
    <p>在终端执行（可选，<code>uvx</code> 首次运行时也会自动拉取）：</p>
    <pre><code>uv tool install blender-mcp</code></pre>
  </div>

  <div class="step">
    <h3>3. 准备 Blender 插件 addon.py</h3>
    <p>插件来自 <code>ahujasid/blender-mcp</code> 仓库，关键文件为 <code>addon.py</code>。在本次配置中：</p>
    <ul>
      <li>原始位置：<code>/tmp/blender-mcp/addon.py</code>（通过 git clone 得到）</li>
      <li>复制到工作区：<code>~/ .openclaw/workspace/blender_mcp_addon.py</code></li>
    </ul>
    <p>你可以通过类似命令完成复制（如尚未复制）：</p>
    <pre><code>cp /tmp/blender-mcp/addon.py \
  ~/.openclaw/workspace/blender_mcp_addon.py</code></pre>
  </div>

  <hr />

  <h2>三、在 Blender 中安装 MCP 插件</h2>

  <div class="step">
    <h3>1. 启动 Blender 4.2</h3>
    <pre><code>/Applications/Blender4.2.app/Contents/MacOS/Blender</code></pre>
  </div>

  <div class="step">
    <h3>2. 安装 addon.py</h3>
    <ol>
      <li>菜单栏选择：<strong>Edit → Preferences…</strong></li>
      <li>左侧选择 <strong>Add-ons</strong></li>
      <li>右上角点击 <strong>Install…</strong></li>
      <li>在文件选择对话框中，选择：<br><code>~/ .openclaw/workspace/blender_mcp_addon.py</code></li>
      <li>安装后，在搜索框中输入 <code>Blender MCP</code></li>
      <li>勾选前面的复选框，启用插件：<strong>Interface: Blender MCP</strong></li>
    </ol>
  </div>

  <div class="step">
    <h3>3. 在 Blender 视图中启动 MCP 连接</h3>
    <ol>
      <li>回到 3D 视图窗口</li>
      <li>按键盘 <code>N</code>，打开右侧侧边栏</li>
      <li>找到名为 <strong>BlenderMCP</strong> 的面板标签</li>
      <li>在该面板中，点击类似 <strong>Connect to Claude</strong> 或 <strong>Start Server</strong> 的按钮</li>
    </ol>
    <p>默认情况下，<code>addon.py</code> 会在本机开启一个 TCP 服务：</p>
    <ul>
      <li>地址：<code>localhost</code></li>
      <li>端口：<code>9876</code></li>
    </ul>
    <p>这就是 MCP Server 将要连接的目标。</p>
  </div>

  <hr />

  <h2>四、配置 mcporter 的 Blender MCP Server</h2>

  <p>mcporter 的全局配置文件位于：</p>
  <pre><code>~/.mcporter/mcporter.json</code></pre>

  <p>在本次配置中，该文件的内容为：</p>

  <pre><code>{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": [
        "blender-mcp"
      ],
      "description": "Blender MCP server (Python) - requires Blender addon"
    }
  },
  "imports": []
}
</code></pre>

  <p>含义说明：</p>
  <ul>
    <li><code>blender</code>：MCP server 名称，后续调用时会用到（如 <code>blender.get_scene_info</code>）。</li>
    <li><code>command: "uvx"</code>：通过 uv 的 <code>uvx</code> 启动一次性命令。</li>
    <li><code>args: ["blender-mcp"]</code>：实际执行命令为 <code>uvx blender-mcp</code>。</li>
    <li><code>description</code>：描述信息，用于标注这是 Python 版 Blender MCP server。</li>
  </ul>

  <div class="note">
    <p><strong>注意：</strong>之前环境中曾使用过一个 TypeScript 版本的 Blender MCP Server（<code>@glutamateapp/blender-mcp-ts</code>），但最终我们改为使用 Python 版 <code>blender-mcp</code>，因为它与 <code>addon.py</code> 官方仓库配套，兼容性更好。</p>
  </div>

  <p>你可以通过以下命令验证配置：</p>

  <pre><code>mcporter config list</code></pre>

  <p>输出示例：</p>

  <pre><code>blender
  Source: local (~/.mcporter/mcporter.json)
  Transport: stdio (uvx blender-mcp)
  CWD: ~/.mcporter
  Description: Blender MCP server (Python) - requires Blender addon

Project config: ~/.openclaw/workspace/config/mcporter.json (missing)
System config: ~/.mcporter/mcporter.json
</code></pre>

  <hr />

  <h2>五、测试连接：获取场景信息</h2>

  <p>在确保 <strong>Blender 已打开</strong> 且 <strong>BlenderMCP 插件已连接</strong> 的前提下，可以使用下面的命令测试 MCP 链路是否正常：</p>

  <pre><code>mcporter call blender.get_scene_info \
  --args '{"user_prompt":"just inspect current scene"}' \
  --output json
</code></pre>

  <p>如果一切正常，会看到类似：</p>

  <pre><code>{
  "content": [
    {
      "type": "text",
      "text": "...场景信息..."
    }
  ],
  "isError": false
}
</code></pre>

  <p>同时，终端中还会看到 <code>blender-mcp</code> 服务器的一些日志，例如：</p>

  <pre><code>BlenderMCPServer - INFO - Connected to Blender at localhost:9876
BlenderMCPServer - INFO - Successfully connected to Blender on startup
BlenderMCPServer - INFO - Processing request of type CallToolRequest
...</code></pre>

  <hr />

  <h2>六、通过 MCP 在 Blender 中生成一个球体</h2>

  <p>核心思想：调用 MCP 工具 <code>execute_blender_code</code>，让它在 Blender 内执行一段 <code>bpy</code> 代码。</p>

  <h3>1. 调用命令示例</h3>

  <p>在终端 / OpenClaw 执行：</p>

  <pre><code>mcporter call blender.execute_blender_code \
  --args '{
    "code": "import bpy; bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0,0,0))",
    "user_prompt": "add a UV sphere at origin"
  }' \
  --output json
</code></pre>

  <p>其中：</p>
  <ul>
    <li><code>code</code> 字段是会在 Blender 内执行的 Python 代码：</li>
  </ul>

  <pre><code>import bpy
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
</code></pre>

  <ul>
    <li><code>user_prompt</code> 是给 MCP Server 用来记录/理解用途的人类可读说明。</li>
  </ul>

  <h3>2. 预期结果</h3>

  <p>命令成功后，会收到类似响应：</p>

  <pre><code>{
  "content": [
    {
      "type": "text",
      "text": "Code executed successfully: "
    }
  ],
  "structuredContent": {
    "result": "Code executed successfully: "
  },
  "isError": false
}
</code></pre>

  <p>同时，Blender 的日志中也会出现：</p>

  <pre><code>BlenderMCPServer - INFO - Sending command: execute_code with params: {...}
BlenderMCPServer - INFO - Response parsed, status: success
</code></pre>

  <p>在 Blender 中：</p>
  <ul>
    <li>3D 视图里，在世界原点 <code>(0, 0, 0)</code> 附近会出现一个 UV Sphere。</li>
    <li>右侧 Outliner 中，会多出一个对应的 Sphere 对象。</li>
  </ul>

  <hr />

  <h2>七、从「自然语言」到「MCP 调用」的链路（简述）</h2>

  <p>当你在 OpenClaw 里说：<strong>“帮我在 Blender 里建一个球体”</strong> 时，背后实际上发生了：</p>

  <ol>
    <li>OpenClaw 根据你的描述，构造出对 MCP Server 的调用：
      <ul>
        <li>Server：<code>blender</code></li>
        <li>Tool：<code>execute_blender_code</code></li>
        <li>Args：包含一段 <code>bpy</code> Python 脚本</li>
      </ul>
    </li>
    <li><code>mcporter</code> 将该调用发送给 <code>uvx blender-mcp</code> 启动的 Python MCP Server。</li>
    <li>Python MCP Server 通过 TCP 连接（<code>localhost:9876</code>）把命令转发给 Blender 插件。</li>
    <li>Blender 插件在 Blender 进程内部执行这段 Python 代码，真正调用 <code>bpy.ops.mesh.primitive_uv_sphere_add(...)</code> 创建球体。</li>
  </ol>

  <p>这就是「OpenClaw → MCP → 本地 Blender → 场景对象」的完整闭环。</p>

  <hr />

  <h2>八、常见问题提示</h2>

  <ul>
    <li><strong>看不到对象？</strong> 可能对象在视野外：在 Outliner 中选中对象，按 <code>.</code> 或使用 <em>Frame Selected</em> 对视图对准。</li>
    <li><strong>MCP Server 报错找不到模块？</strong> 检查 <code>uv</code> 与 <code>blender-mcp</code> 是否安装完整。</li>
    <li><strong>连接不上 Blender？</strong> 确认 Blender 已开启，<code>Blender MCP</code> 插件已启用，并点击了连接按钮，且端口（默认 9876）匹配。</li>
  </ul>

  <p class="ok">到这里，你已经有了一个「OpenClaw 调用本地 Blender 并生成球体」的完整 Demo，可以在此基础上扩展出更多自动化建模操作。</p>
</body>
</html>
