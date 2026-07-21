import unreal


MAP_PATH = "/Game/Maps/L_ZDH_House01_Greybox"
MAT_DIR = "/Game/ProjectCore/Facility/Materials"


def make_dir(path):
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)


def create_material(name, color):
    make_dir(MAT_DIR)
    path = f"{MAT_DIR}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        unreal.EditorAssetLibrary.delete_asset(path)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material = asset_tools.create_asset(
        name,
        MAT_DIR,
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
    roughness.set_editor_property("r", 0.88)
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


def spawn_wall_box(label, location, scale, material):
    return spawn_cube(label, location, scale, material)


def spawn_room_shell(label, center, size, wall_height, material_floor, material_wall, material_trim):
    x, y, z = center
    sx, sy = size
    floor_z = z
    wall_z = z + wall_height / 2.0

    spawn_cube(f"{label}_Floor", (x, y, floor_z), (sx / 100.0, sy / 100.0, 0.08), material_floor)
    spawn_cube(f"{label}_Ceiling", (x, y, z + wall_height), (sx / 100.0, sy / 100.0, 0.06), material_trim)
    spawn_wall_box(f"{label}_Wall_Left", (x - sx / 2.0, y, wall_z), (0.16, sy / 100.0, wall_height / 100.0), material_wall)
    spawn_wall_box(f"{label}_Wall_Right", (x + sx / 2.0, y, wall_z), (0.16, sy / 100.0, wall_height / 100.0), material_wall)
    spawn_wall_box(f"{label}_Wall_Back", (x, y + sy / 2.0, wall_z), (sx / 100.0, 0.16, wall_height / 100.0), material_wall)


def spawn_door_marker(label, location, material):
    spawn_cube(label, location, (1.8, 0.08, 2.2), material)


def spawn_label_marker(label, location, material):
    spawn_cube(label, location, (0.45, 0.45, 0.45), material)


def main():
    for path in [
        "/Game/ProjectCore",
        "/Game/ProjectCore/Facility",
        "/Game/ProjectCore/Facility/Rooms",
        "/Game/ProjectCore/Facility/Corridors",
        "/Game/ProjectCore/Facility/Connectors",
        "/Game/ProjectCore/Facility/Materials",
        "/Game/ProjectCore/Facility/Debug",
        "/Game/ProjectCore/Maps",
        "/Game/Maps",
    ]:
        make_dir(path)

    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        unreal.EditorLevelLibrary.load_level(MAP_PATH)
    else:
        unreal.EditorLevelLibrary.new_level(MAP_PATH)
    clear_level()

    mat_ground = create_material("M_PC_Blockout_Ground", (0.16, 0.18, 0.17, 1.0))
    mat_concrete = create_material("M_PC_Blockout_Concrete", (0.48, 0.50, 0.48, 1.0))
    mat_wall = create_material("M_PC_Blockout_FacilityWall", (0.58, 0.63, 0.61, 1.0))
    mat_dark = create_material("M_PC_Blockout_DarkMetal", (0.10, 0.11, 0.12, 1.0))
    mat_door = create_material("M_PC_Blockout_Door", (0.42, 0.39, 0.30, 1.0))
    mat_glass = create_material("M_PC_Blockout_Glass", (0.10, 0.32, 0.45, 1.0))
    mat_warning = create_material("M_PC_Blockout_Warning", (0.90, 0.55, 0.05, 1.0))
    mat_blue = create_material("M_PC_Blockout_PlayerStart", (0.05, 0.22, 0.85, 1.0))
    mat_red = create_material("M_PC_Blockout_ThreatMarker", (0.75, 0.04, 0.03, 1.0))
    mat_lower = create_material("M_PC_Blockout_LowerLevel", (0.30, 0.33, 0.36, 1.0))

    # Exterior staging area and Lethal Company style facility facade.
    spawn_cube("Exterior_Ground_RecoveryZone", (0.0, -900.0, -5.0), (42.0, 32.0, 0.10), mat_ground)
    spawn_cube("Recovery_Vehicle_Pad", (-900.0, -1600.0, 0.0), (7.5, 5.0, 0.06), mat_concrete)
    spawn_cube("Approach_Road", (0.0, -1550.0, 2.0), (6.0, 10.0, 0.04), mat_concrete)
    spawn_cube("Facility_Front_Apron", (0.0, -760.0, 4.0), (14.0, 4.0, 0.05), mat_concrete)

    # Single-storey entrance building. No second-floor house silhouette.
    spawn_cube("Facility_Entrance_Foundation", (0.0, -360.0, 8.0), (18.0, 7.5, 0.16), mat_concrete)
    spawn_cube("Facility_Entrance_Roof", (0.0, -360.0, 345.0), (18.8, 8.2, 0.28), mat_dark)
    spawn_cube("Facility_Front_Wall_Left", (-530.0, -740.0, 155.0), (7.2, 0.18, 2.8), mat_wall)
    spawn_cube("Facility_Front_Wall_Right", (530.0, -740.0, 155.0), (7.2, 0.18, 2.8), mat_wall)
    spawn_cube("Facility_Back_Wall", (0.0, 20.0, 155.0), (18.0, 0.18, 2.8), mat_wall)
    spawn_cube("Facility_Left_Wall", (-900.0, -360.0, 155.0), (0.18, 7.6, 2.8), mat_wall)
    spawn_cube("Facility_Right_Wall", (900.0, -360.0, 155.0), (0.18, 7.6, 2.8), mat_wall)
    spawn_cube("Main_Containment_Door", (0.0, -755.0, 125.0), (2.2, 0.12, 2.4), mat_door)
    spawn_cube("Reception_Window_Left", (-430.0, -760.0, 180.0), (2.2, 0.07, 1.0), mat_glass)
    spawn_cube("Reception_Window_Right", (430.0, -760.0, 180.0), (2.2, 0.07, 1.0), mat_glass)
    spawn_cube("Facility_Sign_Blockout", (0.0, -780.0, 290.0), (4.8, 0.05, 0.55), mat_warning)

    # Interior main axis extends backward into the site.
    corridor_y_values = [260.0, 900.0, 1540.0, 2180.0]
    for index, y in enumerate(corridor_y_values):
        spawn_cube(f"Main_Corridor_{index + 1}_Floor", (0.0, y, 12.0), (5.2, 6.4, 0.08), mat_concrete)
        spawn_cube(f"Main_Corridor_{index + 1}_Ceiling", (0.0, y, 330.0), (5.2, 6.4, 0.05), mat_dark)
        spawn_cube(f"Main_Corridor_{index + 1}_LeftWall", (-260.0, y, 160.0), (0.12, 6.4, 2.8), mat_wall)
        spawn_cube(f"Main_Corridor_{index + 1}_RightWall", (260.0, y, 160.0), (0.12, 6.4, 2.8), mat_wall)

    # Side rooms and believable facility branches.
    spawn_room_shell("Security_Checkpoint_Left", (-760.0, 320.0, 12.0), (760.0, 560.0), 300.0, mat_concrete, mat_wall, mat_dark)
    spawn_door_marker("Door_Security_Checkpoint", (-270.0, 320.0, 125.0), mat_door)
    spawn_room_shell("Admin_Records_Right", (760.0, 780.0, 12.0), (760.0, 600.0), 300.0, mat_concrete, mat_wall, mat_dark)
    spawn_door_marker("Door_Admin_Records", (270.0, 780.0, 125.0), mat_door)
    spawn_room_shell("Medical_Triage_Left", (-820.0, 1360.0, 12.0), (880.0, 620.0), 300.0, mat_concrete, mat_wall, mat_dark)
    spawn_door_marker("Door_Medical_Triage", (-270.0, 1360.0, 125.0), mat_door)
    spawn_room_shell("Research_Lab_Right", (860.0, 1620.0, 12.0), (960.0, 700.0), 300.0, mat_concrete, mat_wall, mat_dark)
    spawn_door_marker("Door_Research_Lab", (270.0, 1620.0, 125.0), mat_door)
    spawn_room_shell("Maintenance_Access_Left", (-760.0, 2260.0, 12.0), (760.0, 600.0), 300.0, mat_concrete, mat_wall, mat_dark)
    spawn_door_marker("Door_Maintenance_Access", (-270.0, 2260.0, 125.0), mat_door)
    spawn_room_shell("Containment_Antechamber_Right", (900.0, 2420.0, 12.0), (1040.0, 760.0), 300.0, mat_concrete, mat_wall, mat_dark)
    spawn_door_marker("Door_Containment_Antechamber", (270.0, 2420.0, 125.0), mat_door)

    # One lower floor descent only: a ramp/stairwell leading to a lower service corridor.
    spawn_cube("Lower_Level_Stairwell_Frame", (-760.0, 2860.0, 15.0), (8.0, 5.8, 0.08), mat_lower)
    spawn_cube("Lower_Level_Ramp_Down", (-760.0, 2860.0, -80.0), (4.8, 6.2, 0.20), mat_warning, rotation=(0.0, -14.0, 0.0))
    spawn_cube("Lower_Service_Corridor_Floor", (-760.0, 3440.0, -190.0), (5.0, 7.0, 0.08), mat_lower)
    spawn_cube("Lower_Service_Corridor_LeftWall", (-1010.0, 3440.0, -45.0), (0.12, 7.0, 2.6), mat_wall)
    spawn_cube("Lower_Service_Corridor_RightWall", (-510.0, 3440.0, -45.0), (0.12, 7.0, 2.6), mat_wall)
    spawn_cube("Lower_Service_Corridor_Ceiling", (-760.0, 3440.0, 110.0), (5.0, 7.0, 0.05), mat_dark)

    # Debug markers for later procedural generator sockets and zones.
    spawn_label_marker("DEBUG_SOCKET_Entrance_In", (0.0, -960.0, 60.0), mat_blue)
    spawn_label_marker("DEBUG_SOCKET_MainAxis_A", (0.0, 580.0, 60.0), mat_warning)
    spawn_label_marker("DEBUG_SOCKET_MainAxis_B", (0.0, 1220.0, 60.0), mat_warning)
    spawn_label_marker("DEBUG_SOCKET_MainAxis_C", (0.0, 1860.0, 60.0), mat_warning)
    spawn_label_marker("DEBUG_SOCKET_LowerRamp", (-760.0, 3020.0, -80.0), mat_warning)
    spawn_label_marker("ThreatSpawn_Debug_DeepFacility", (600.0, 2500.0, 60.0), mat_red)

    player_start_marker = spawn_label_marker("PlayerStart_Marker_RecoveryTeam", (0.0, -1450.0, 35.0), mat_blue)
    player_start = spawn_actor(unreal.PlayerStart, "PlayerStart_RecoveryTeam", (0.0, -1450.0, 105.0), (0.0, 0.0, 0.0))
    player_start.set_actor_rotation(unreal.Rotator(0.0, 90.0, 0.0), False)

    sun = spawn_actor(unreal.DirectionalLight, "Sun_Exterior_Overcast", (-800.0, -1200.0, 1300.0), (-38.0, -25.0, 0.0))
    make_movable(sun)
    sun_component = sun.get_component_by_class(unreal.DirectionalLightComponent)
    if sun_component:
        sun_component.set_editor_property("intensity", 2.0)

    sky_light = spawn_actor(unreal.SkyLight, "SkyLight_ColdFacility", (0.0, 0.0, 700.0))
    make_movable(sky_light)
    sky_component = sky_light.get_component_by_class(unreal.SkyLightComponent)
    if sky_component:
        sky_component.set_editor_property("intensity", 1.1)

    for optional_class, label, location in [
        (getattr(unreal, "SkyAtmosphere", None), "SkyAtmosphere_Main", (0.0, 0.0, 0.0)),
        (getattr(unreal, "ExponentialHeightFog", None), "Fog_LightFacilityFill", (0.0, 0.0, 0.0)),
    ]:
        if optional_class:
            spawn_actor(optional_class, label, location)

    nav = spawn_actor(unreal.NavMeshBoundsVolume, "NavMeshBounds_Facility", (0.0, 1300.0, 80.0))
    nav.set_actor_scale3d(unreal.Vector(24.0, 44.0, 5.0))

    unreal.EditorLevelLibrary.set_level_viewport_camera_info(
        unreal.Vector(2100.0, -2500.0, 1150.0),
        unreal.Rotator(-24.0, 0.0, 38.0),
    )
    unreal.EditorLevelLibrary.save_current_level()
    unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    unreal.log("ProjectCore facility entrance blockout setup complete.")


main()
