# Blueprint Foundation v0.1

The project is Blueprint-first. C++ exists only as a small replicated backbone.

## C++ Parents

Create Blueprint child assets from these classes:

- `AZDHPlayerCharacter`
- `AZDHZombieCharacter`
- `AZDHBarricade`
- `AZDHWeaponBase`
- `AZDHGameMode`
- `AZDHGameState`
- `AZDHPlayerController`
- `AZDHPlayerState`

## First Blueprint Assets

### Player

- `/Game/Characters/Player/BP_PlayerCharacter_Base`
- `/Game/Characters/Player/BP_Player_Assault`
- `/Game/Characters/Player/BP_Player_Medic`
- `/Game/Characters/Player/BP_Player_Engineer`

Parent: `AZDHPlayerCharacter`

### Zombies

- `/Game/Characters/Zombies/BP_Zombie_Base`
- `/Game/Characters/Zombies/BP_Zombie_Walker`

Parent: `AZDHZombieCharacter`

### Defense

- `/Game/Environment/Barricades/BP_Barricade_Base`
- `/Game/Environment/Barricades/BP_Barricade_Window_Wood`

Parent: `AZDHBarricade`

### Weapons

- `/Game/Items/Weapons/BP_Weapon_Base`
- `/Game/Items/Weapons/BP_Weapon_Pistol`
- `/Game/Items/Weapons/BP_Weapon_PumpShotgun`

Parent: `AZDHWeaponBase`

### Core

- `/Game/Core/BP_ZDHGameMode`
- `/Game/Core/BP_ZDHGameState`
- `/Game/Core/BP_ZDHPlayerController`
- `/Game/Core/BP_ZDHPlayerState`

Parents: matching C++ core classes.

## First Playable Loop

1. Player spawns in greybox house.
2. Zombie spawns outside.
3. Zombie moves toward barricade.
4. Zombie damages barricade.
5. Player repairs barricade.
6. Player shoots zombie.
7. Zombie dies and rewards are added later through PlayerState.

## Blueprint Rules

- No hardcoded balance values inside event graphs.
- Use exposed variables first, DataTables/DataAssets later.
- Server-authoritative gameplay.
- Cosmetic/audio/UI logic can be client-side.
- Every base Blueprint must be small and readable.

