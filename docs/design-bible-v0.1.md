# Zombie Defense House - Design Bible v0.1

## Vision

Zombie Defense House is a 1-6 player co-op survival defense game for Steam.
Players defend a vulnerable house against escalating zombie waves by fighting,
repairing barricades, managing resources, and combining class roles.

The game mixes:

- Left 4 Dead style team pressure and special zombie threats.
- CoD Zombies style waves, money, weapon progression, and perk growth.
- A house defense identity built around barricades, infection, resource tension,
  and replayable layouts.

This is not a prototype-first toy project. Every system must be built with
multiplayer, tuning, and long-term maintainability in mind.

## Core Pillars

1. Team survival under pressure.
2. Defend, repair, reposition, and adapt.
3. Data-driven progression and replayability.
4. Blueprint-friendly production with a small C++ multiplayer core.
5. Clear Steam-ready identity: tense co-op zombie house defense.

## Player Fantasy

Players are trapped in a hostile house at night. Every wave makes the house feel
less safe. Windows break, doors fail, ammunition runs low, infection rises, and
the team has to decide whether to hold, repair, loot, or retreat upstairs.

The best moments should feel like:

- "Hold this hallway for ten more seconds."
- "Medic, I am infected."
- "Repair that window or we are surrounded."
- "Save money for the next room or buy ammo now?"
- "The brute is at the back door."

## Target Experience

- Camera: First person.
- Players: 1-6 co-op, initial test target 1-2.
- Session type: Listen server first, Steam lobby later.
- Tone: dark, grounded, intense, arcade-readable.
- Match length target: 20-40 minutes.
- Replay hooks: class roles, random perk choices, wave scaling, elite weapons,
  loot variation, alternate entry points.

## Core Loop

1. Preparation starts.
2. Players repair barricades, buy ammo, open rooms, and choose upgrades.
3. Wave starts.
4. Zombies attack players or barricades.
5. Players earn money, XP, and materials by surviving and killing.
6. Infection, ammo, and barricade damage create pressure.
7. Wave ends.
8. Rewards and difficulty scale.
9. Repeat until extraction, boss wave, or team wipe.

## First Vertical Slice

The first playable slice must be small, stable, and multiplayer-safe.

Required:

- One test map.
- One player character.
- One basic weapon.
- One zombie type.
- One barricade.
- One interact/repair flow.
- One wave manager.
- One basic HUD.
- Two-player listen server test.

Not required yet:

- Full Steam integration.
- Multiple classes.
- Full skill tree.
- Boss zombies.
- Final art.
- Large house map.

## Technical Direction

### C++ Core

Use C++ for systems where multiplayer correctness matters:

- GameMode.
- GameState.
- PlayerController.
- PlayerState.
- replicated stat storage.
- session/lobby wrapper later.
- authority-only wave manager later.

### Blueprint Production

Use Blueprint for most gameplay authoring:

- player child Blueprint.
- zombie behavior tuning.
- weapons.
- barricades.
- UI widgets.
- interactables.
- map logic.
- DataTable/DataAsset driven values.

### MCP/AI Usage

MCP is a production assistant, not the game designer.

Use MCP for:

- creating folders/assets.
- spawning test objects.
- running editor scripts.
- generating repetitive Blueprint setup.
- inspecting project state.
- creating DataTables/DataAssets.

Do not use MCP for:

- uncontrolled random Blueprint graphs.
- unexplained multiplayer logic.
- hardcoded balance values.
- changes without verification.

## Data-Driven Rule

No important gameplay value should be permanently hardcoded.

Use configurable data for:

- zombie HP.
- zombie speed.
- zombie damage.
- wave count.
- spawn rate.
- player HP.
- infection rate.
- repair cost.
- weapon damage.
- perk values.
- material reward.
- money reward.

## Initial Classes

### Assault

Damage and ammo-focused. Simple, reliable first combat class.

### Medic

Can heal teammates and reduce infection using injector-style equipment.

### Engineer

Repairs faster, uses fewer materials, and can reinforce barricades.

Only Assault or a generic survivor is required for the first vertical slice.

## Initial Zombie Types

### Walker

Basic slow zombie. Teaches combat and barricade pressure.

### Runner

Fast zombie. Forces target switching and panic.

### Brute

High HP threat. Attacks barricades and blocks space.

Only Walker is required for the first vertical slice.

## Infection

Zombie attacks increase player infection.

At 100 percent infection:

- the player starts losing health over time.
- the UI must clearly warn the player.
- Medic tools or rare consumables can reduce infection.

Infection should create time pressure without instantly killing fun.

## Barricades

Barricades are the house defense identity.

Each barricade has:

- HP.
- damaged visual states.
- repair interaction.
- material cost.
- replicated repair progress.
- zombie target priority.

First slice only needs one barricaded window.

## Wave Scaling

Initial formula direction:

```text
ScaledValue = BaseValue + (BaseValue * PlayerCount * DifficultyMultiplier)
```

Used for:

- zombie count.
- zombie HP.
- reward scaling.

All values must live in tunable data.

## Steam/Elite Direction

Steam is not part of the first slice.

Later:

- Steam lobby.
- friend invite.
- Steam ID lookup.
- Elite player DataTable.
- special melee weapon spawn for matching Steam IDs.

## Immediate Next Steps

1. Verify UE project opens cleanly.
2. Verify official UE MCP and/or Remote Control is reachable.
3. Create `/Game` folder skeleton inside the editor.
4. Create initial test map `L_ZDH_Startup`.
5. Create Blueprint base asset plan.
6. Build the first playable test loop.

