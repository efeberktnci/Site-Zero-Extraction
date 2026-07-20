# Phase 0 MCP Setup

## Recommended Route

Use Unreal Engine 5.8 official Unreal MCP when available. It runs inside the editor,
binds locally by default at `http://127.0.0.1:8000/mcp`, and serializes tool calls on
the Unreal game thread.

Fallback bridge in this repo:

- `tools/mcp/zdh_mcp_server.py`: local MCP server for project operations and connection checks.
- `tools/unreal/spawn_test_cube.py`: Unreal Python script that spawns the validation cube.
- `tools/unreal/create_project_skeleton.py`: Unreal Python script that creates `/Game` folders.

## Unreal Plugins

Enable these in the Unreal Editor:

- Model Context Protocol, when using UE 5.8 official MCP.
- Remote Control API.
- Python Editor Script Plugin.
- Editor Scripting Utilities.

## Local MCP Server

```powershell
cd "D:\Zombie Game"
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tools\mcp\requirements.txt
.\.venv\Scripts\python.exe tools\mcp\zdh_mcp_server.py
```

## First Validation

When Unreal is open and Remote Control API is enabled:

```powershell
curl http://127.0.0.1:30010/remote/info
```

Then run `tools/unreal/spawn_test_cube.py` through Unreal Python or the official MCP
Python execution tool.
