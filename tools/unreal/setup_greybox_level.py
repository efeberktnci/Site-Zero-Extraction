import unreal


MAP_PATH = "/Game/Maps/L_ZDH_House01_Greybox"


def make_dir(path):
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)


def create_material(name, color):
    path = f"/Game/Environment/House/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        unreal.EditorAssetLibrary.delete_asset(path)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material = asset_tools.create_asset(
        name,
        "/Game/Environment/House",
        unreal.Material,
        unreal.MaterialFactoryNew(),
    )

    color_node = unreal.MaterialEditingLibrary.create_material_expression(
        material,
        unreal.MaterialExpressionConstant3Vector,
        -400,
        0,
    )
    color_node.set_editor_property("constant", unreal.LinearColor(*color))
    unreal.MaterialEditingLibrary.connect_material_property(
        color_node,
        "",
        unreal.MaterialProperty.MP_BASE_COLOR,
    )

    roughness = unreal.MaterialEditingLibrary.create_material_expression(
        material,
        unreal.MaterialExpressionConstant,
        -400,
        180,
    )
    roughness.set_editor_property("r", 0.9)
    unreal.MaterialEditingLibrary.connect_material_property(
        roughness,
        "",
        unreal.MaterialProperty.MP_ROUGHNESS,
    )

    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material)
    return material


def set_mesh_material(actor, material):
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component and material:
        component.set_material(0, material)


def spawn_cube(label, location, scale, material=None, rotation=(0.0, 0.0, 0.0)):
    mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
        mesh,
        unreal.Vector(*location),
        unreal.Rotator(*rotation),
    )
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    set_mesh_material(actor, material)
    return actor


def make_movable(actor):
    for component in actor.get_components_by_class(unreal.SceneComponent):
        if hasattr(component, "set_mobility"):
            component.set_mobility(unreal.ComponentMobility.MOVABLE)


def spawn_actor(actor_class, label, location, rotation=(0.0, 0.0, 0.0)):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        actor_class,
        unreal.Vector(*location),
        unreal.Rotator(*rotation),
    )
    actor.set_actor_label(label)
    return actor


def clear_level():
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        unreal.EditorLevelLibrary.destroy_actor(actor)


def main():
    for path in [
        "/Game/Core",
        "/Game/Characters/Player",
        "/Game/Characters/Zombies",
        "/Game/AI",
        "/Game/UI",
        "/Game/Items/Weapons",
        "/Game/Items/Resources",
        "/Game/Environment/House",
        "/Game/Environment/Barricades",
        "/Game/Maps",
        "/Game/Data",
        "/Game/Blueprints/Base",
        "/Game/Blueprints/Interactables",
    ]:
        make_dir(path)

    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        unreal.EditorLevelLibrary.load_level(MAP_PATH)
    else:
        unreal.EditorLevelLibrary.new_level(MAP_PATH)
    clear_level()

    mat_grass = create_material("M_Blockout_Grass", (0.18, 0.42, 0.14, 1.0))
    mat_concrete = create_material("M_Blockout_Concrete", (0.58, 0.58, 0.54, 1.0))
    mat_wall = create_material("M_Blockout_WarmWall", (0.74, 0.77, 0.72, 1.0))
    mat_trim = create_material("M_Blockout_DarkTrim", (0.12, 0.13, 0.12, 1.0))
    mat_roof = create_material("M_Blockout_Roof", (0.24, 0.25, 0.26, 1.0))
    mat_glass = create_material("M_Blockout_Window", (0.16, 0.35, 0.55, 1.0))
    mat_wood = create_material("M_Blockout_Wood", (0.46, 0.25, 0.10, 1.0))
    mat_spawn = create_material("M_Blockout_ZombieSpawn", (0.75, 0.05, 0.03, 1.0))
    mat_player = create_material("M_Blockout_PlayerStart", (0.05, 0.22, 0.85, 1.0))

    # World scale: 1 Unreal unit = 1 cm. This yard is 42m x 34m.
    spawn_cube("Yard_Grass_42x34m", (0.0, 0.0, -5.0), (42.0, 34.0, 0.10), mat_grass)
    spawn_cube("Driveway_Concrete", (-1250.0, -900.0, 0.0), (8.0, 12.0, 0.05), mat_concrete)
    spawn_cube("Front_Walkway", (0.0, -1030.0, 2.0), (3.0, 6.5, 0.04), mat_concrete)

    # Simple two-floor detached house, readable from outside.
    spawn_cube("House_Foundation", (0.0, 0.0, 8.0), (18.4, 14.4, 0.16), mat_concrete)
    spawn_cube("Floor_01_Interior", (0.0, 0.0, 18.0), (17.4, 13.4, 0.06), mat_concrete)
    spawn_cube("Floor_02_Interior", (0.0, 0.0, 342.0), (17.4, 13.4, 0.06), mat_concrete)

    # First-floor exterior walls.
    spawn_cube("Wall_F01_Front_Left", (-480.0, -700.0, 155.0), (7.2, 0.22, 2.7), mat_wall)
    spawn_cube("Wall_F01_Front_Right", (480.0, -700.0, 155.0), (7.2, 0.22, 2.7), mat_wall)
    spawn_cube("Wall_F01_Back", (0.0, 700.0, 155.0), (18.0, 0.22, 2.7), mat_wall)
    spawn_cube("Wall_F01_Left", (-900.0, 0.0, 155.0), (0.22, 14.0, 2.7), mat_wall)
    spawn_cube("Wall_F01_Right", (900.0, 0.0, 155.0), (0.22, 14.0, 2.7), mat_wall)

    # Second-floor exterior walls.
    spawn_cube("Wall_F02_Front", (0.0, -700.0, 455.0), (18.0, 0.20, 2.5), mat_wall)
    spawn_cube("Wall_F02_Back", (0.0, 700.0, 455.0), (18.0, 0.20, 2.5), mat_wall)
    spawn_cube("Wall_F02_Left", (-900.0, 0.0, 455.0), (0.20, 14.0, 2.5), mat_wall)
    spawn_cube("Wall_F02_Right", (900.0, 0.0, 455.0), (0.20, 14.0, 2.5), mat_wall)

    # Roof reads as roof instead of one giant white gameplay floor.
    spawn_cube("Roof_Main_Blockout", (0.0, 0.0, 610.0), (19.2, 15.2, 0.35), mat_roof)
    spawn_cube("Roof_Ridge_Marker", (0.0, 0.0, 675.0), (19.0, 0.28, 0.28), mat_trim)

    # Doors/windows/barricade positions. These are flat markers for later Blueprint replacements.
    spawn_cube("Front_Door_Blockout", (0.0, -715.0, 110.0), (1.5, 0.08, 2.1), mat_wood)
    spawn_cube("Window_Front_Left_BarricadeSlot", (-520.0, -725.0, 170.0), (2.0, 0.08, 1.1), mat_glass)
    spawn_cube("Window_Front_Right_BarricadeSlot", (520.0, -725.0, 170.0), (2.0, 0.08, 1.1), mat_glass)
    spawn_cube("Window_Back_Left_BarricadeSlot", (-520.0, 725.0, 170.0), (2.0, 0.08, 1.1), mat_glass)
    spawn_cube("Window_Back_Right_BarricadeSlot", (520.0, 725.0, 170.0), (2.0, 0.08, 1.1), mat_glass)
    spawn_cube("Window_F02_Front_Left", (-520.0, -725.0, 470.0), (1.8, 0.08, 1.0), mat_glass)
    spawn_cube("Window_F02_Front_Right", (520.0, -725.0, 470.0), (1.8, 0.08, 1.0), mat_glass)

    # Interior gameplay markers.
    spawn_cube("Interior_Wall_Hallway", (-150.0, 0.0, 155.0), (0.16, 9.0, 2.4), mat_wall)
    spawn_cube("Interior_Wall_Kitchen", (300.0, 160.0, 155.0), (5.5, 0.16, 2.4), mat_wall)
    spawn_cube("Staircase_Blockout", (560.0, 250.0, 125.0), (2.2, 4.2, 1.2), mat_wood)

    # Spawn markers.
    spawn_cube("ZombieSpawn_FrontYard", (0.0, -1450.0, 35.0), (0.55, 0.55, 0.55), mat_spawn)
    spawn_cube("ZombieSpawn_BackYard", (0.0, 1450.0, 35.0), (0.55, 0.55, 0.55), mat_spawn)
    spawn_cube("ZombieSpawn_LeftYard", (-1500.0, 0.0, 35.0), (0.55, 0.55, 0.55), mat_spawn)
    spawn_cube("PlayerStart_Marker", (0.0, -350.0, 35.0), (0.45, 0.45, 0.45), mat_player)

    player_start = spawn_actor(unreal.PlayerStart, "PlayerStart_Main", (0.0, -350.0, 105.0), (0.0, 0.0, 0.0))
    player_start.set_actor_rotation(unreal.Rotator(0.0, 90.0, 0.0), False)

    sun = spawn_actor(unreal.DirectionalLight, "Sun_Main", (-600.0, -600.0, 1200.0), (-45.0, -35.0, 0.0))
    make_movable(sun)
    sun_component = sun.get_component_by_class(unreal.DirectionalLightComponent)
    if sun_component:
        sun_component.set_editor_property("intensity", 3.2)

    sky_light = spawn_actor(unreal.SkyLight, "SkyLight_Main", (0.0, 0.0, 700.0))
    make_movable(sky_light)
    sky_component = sky_light.get_component_by_class(unreal.SkyLightComponent)
    if sky_component:
        sky_component.set_editor_property("intensity", 1.8)

    for optional_class, label, location in [
        (getattr(unreal, "SkyAtmosphere", None), "SkyAtmosphere_Main", (0.0, 0.0, 0.0)),
        (getattr(unreal, "ExponentialHeightFog", None), "Fog_LightWorldFill", (0.0, 0.0, 0.0)),
    ]:
        if optional_class:
            spawn_actor(optional_class, label, location)

    nav = spawn_actor(unreal.NavMeshBoundsVolume, "NavMeshBounds_Main", (0.0, 0.0, 120.0))
    nav.set_actor_scale3d(unreal.Vector(22.0, 18.0, 4.0))

    unreal.EditorLevelLibrary.set_level_viewport_camera_info(
        unreal.Vector(1700.0, -2100.0, 950.0),
        unreal.Rotator(-24.0, 0.0, 39.0),
    )
    unreal.EditorLevelLibrary.save_current_level()
    unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    unreal.log("ZDH normal-world blockout level setup complete.")


main()
