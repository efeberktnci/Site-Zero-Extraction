# Engine Install Blocker

Codex found no working `UnrealEditor.exe` on this machine.

Current state:

- `winget` reports Epic Games Launcher as installed.
- Windows registry points it to `F:\Epic Games\`.
- The `F:` drive is not mounted, so the launcher executable is not present.
- `winget upgrade/install` failed with MSI exit code `1603`.

Best fix:

1. Uninstall the stale Epic Games Launcher entry from Windows Apps.
2. Install Epic Games Launcher again.
3. Install Unreal Engine 5.8.
4. Re-run `tools/setup/find_unreal.ps1`.

Once `UnrealEditor.exe` exists, the project can be opened with:

```powershell
.\tools\setup\open_project.ps1 -UnrealEditorExe "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
```

