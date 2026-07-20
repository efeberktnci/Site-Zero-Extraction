param(
    [Parameter(Mandatory = $true)]
    [string]$UnrealEditorExe
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$ProjectFile = Join-Path $ProjectRoot "ZombieDefenseHouse.uproject"

if (-not (Test-Path $UnrealEditorExe)) {
    throw "UnrealEditor.exe not found: $UnrealEditorExe"
}

if (-not (Test-Path $ProjectFile)) {
    throw "Project file not found: $ProjectFile"
}

Start-Process -FilePath $UnrealEditorExe -ArgumentList "`"$ProjectFile`"" -WorkingDirectory $ProjectRoot -WindowStyle Hidden

