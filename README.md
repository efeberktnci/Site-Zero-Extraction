# Site Zero Extraction

Unreal Engine 5.8 multiplayer prototype for an asymmetric PvP extraction horror game.

## Project

- Engine: Unreal Engine 5.8
- Project file: `ZombieDefenseHouse.uproject`
- Current working title: `Site Zero Extraction`
- Core direction: humans vs creature players, extraction, infection, barricades, class-based survival.

## Setup

1. Install Unreal Engine 5.8.
2. Install Git LFS.
3. Clone the repository.
4. Run:

```powershell
git lfs install
git lfs pull
```

5. Right-click `ZombieDefenseHouse.uproject` and generate project files if needed.
6. Open `ZombieDefenseHouse.uproject`.

## Repository Rules

Committed:

- `Config/`
- `Content/`
- `Source/`
- `docs/`
- `tools/`
- `ZombieDefenseHouse.uproject`

Not committed:

- `Binaries/`
- `DerivedDataCache/`
- `Intermediate/`
- `Saved/`
- `.vs/`
- local marketplace/source archives under `SourceAssets/Marketplace/`

Imported Unreal assets that are needed by the game should live under `Content/` and are tracked through Git LFS.
