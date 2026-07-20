import unreal


LABEL = "MCP_Phase0_TestCube"
LOCATION = unreal.Vector(0.0, 0.0, 120.0)
SCALE = unreal.Vector(1.0, 1.0, 1.0)


def main():
    editor_level_library = unreal.EditorLevelLibrary
    editor_asset_library = unreal.EditorAssetLibrary

    for actor in editor_level_library.get_all_level_actors():
        if actor.get_actor_label() == LABEL:
            editor_level_library.destroy_actor(actor)

    cube_mesh = editor_asset_library.load_asset("/Engine/BasicShapes/Cube.Cube")
    actor = editor_level_library.spawn_actor_from_object(cube_mesh, LOCATION)
    actor.set_actor_label(LABEL)
    actor.set_actor_scale3d(SCALE)
    unreal.log("Zombie Defense House MCP Phase 0 cube spawned successfully.")
    return actor


main()

