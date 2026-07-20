from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

import requests
from mcp.server.fastmcp import FastMCP


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UE_HTTP = os.environ.get("ZDH_UE_REMOTE_HTTP", "http://127.0.0.1:30010")
UE_MCP_URL = os.environ.get("ZDH_UE_MCP_URL", "http://127.0.0.1:8000/mcp")
UE_PYTHON = os.environ.get("ZDH_UE_PYTHON", "")

mcp = FastMCP("zombie-defense-house")


def _result(ok: bool, message: str, data: Any | None = None) -> dict[str, Any]:
    return {"ok": ok, "message": message, "data": data}


@mcp.tool()
def project_info() -> dict[str, Any]:
    """Return local project and bridge configuration."""
    uprojects = [str(p) for p in PROJECT_ROOT.glob("*.uproject")]
    return _result(
        True,
        "Project bridge configuration loaded.",
        {
            "project_root": str(PROJECT_ROOT),
            "uprojects": uprojects,
            "ue_remote_http": UE_HTTP,
            "ue_mcp_url": UE_MCP_URL,
            "ue_python": UE_PYTHON,
        },
    )


@mcp.tool()
def check_remote_control() -> dict[str, Any]:
    """Check whether Unreal Remote Control HTTP is responding."""
    try:
        response = requests.get(f"{UE_HTTP}/remote/info", timeout=3)
        return _result(
            response.ok,
            f"Remote Control returned HTTP {response.status_code}.",
            response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
        )
    except Exception as exc:
        return _result(False, f"Remote Control is not reachable: {exc}")


@mcp.tool()
def create_project_folders() -> dict[str, Any]:
    """Create the Phase 0 content/source folder skeleton on disk."""
    folders = [
        "Content/Core",
        "Content/Characters",
        "Content/Characters/Player",
        "Content/Characters/Zombies",
        "Content/AI",
        "Content/UI",
        "Content/Items",
        "Content/Maps",
        "Content/Data",
        "Content/Blueprints",
        "Source/ZombieDefenseHouse",
        "Config",
        "Plugins",
    ]
    created = []
    for rel in folders:
        path = PROJECT_ROOT / rel
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))
    return _result(True, "Project folder skeleton is ready.", created)


@mcp.tool()
def spawn_test_cube_script() -> dict[str, Any]:
    """Return the UE Python script path that spawns the Phase 0 test cube."""
    script = PROJECT_ROOT / "tools" / "unreal" / "spawn_test_cube.py"
    return _result(script.exists(), "Run this script inside Unreal Python to spawn the MCP test cube.", str(script))


@mcp.tool()
def open_unreal_project(unreal_editor_path: str, uproject_path: str = "") -> dict[str, Any]:
    """Open the Unreal project with a caller-provided UnrealEditor.exe path."""
    editor = Path(unreal_editor_path)
    if not editor.exists():
        return _result(False, f"UnrealEditor.exe was not found: {editor}")

    project = Path(uproject_path) if uproject_path else next(PROJECT_ROOT.glob("*.uproject"), None)
    if project is None or not project.exists():
        return _result(False, "No .uproject file was found. Create/open the UE project first.")

    subprocess.Popen([str(editor), str(project)], cwd=str(PROJECT_ROOT))
    return _result(True, "Unreal Editor launch requested.", {"editor": str(editor), "project": str(project)})


if __name__ == "__main__":
    mcp.run()

