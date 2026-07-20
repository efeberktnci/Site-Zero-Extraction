$ErrorActionPreference = "SilentlyContinue"

$candidateRoots = @(
    "C:\Program Files\Epic Games",
    "C:\Program Files (x86)\Epic Games",
    "D:\Epic Games",
    "E:\Epic Games",
    "F:\Epic Games",
    "C:\Engine",
    "D:\Engine",
    "E:\Engine",
    "F:\Engine"
)

$editors = @()
foreach ($root in $candidateRoots) {
    if (Test-Path $root) {
        $editors += Get-ChildItem -Path $root -Recurse -Filter UnrealEditor.exe
    }
}

$editors += Get-Command UnrealEditor.exe | ForEach-Object {
    Get-Item $_.Source
}

$editors |
    Sort-Object FullName -Unique |
    Select-Object FullName, VersionInfo |
    Format-Table -AutoSize

if ($editors.Count -eq 0) {
    Write-Host "No UnrealEditor.exe was found on the usual local paths."
}

