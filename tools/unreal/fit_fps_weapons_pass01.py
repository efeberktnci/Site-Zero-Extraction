import unreal

SHOTGUN_BP_PATH = "/Game/Items/Weapons/Blueprints/BP_Weapon_PumpShotgun"
PISTOL_BP_PATH = "/Game/Items/Weapons/Blueprints/BP_Weapon_G17"
CHARACTER_BP_PATH = "/Game/Variant_Shooter/Blueprints/BP_ShooterCharacter"
TARGET_SHOTGUN_LENGTH_CM = 95.0
TARGET_PISTOL_LENGTH_CM = 22.0


def generated_class(path):
    bp = unreal.EditorAssetLibrary.load_asset(path)
    if not bp:
        raise RuntimeError(f"Could not load blueprint: {path}")
    return bp, bp.generated_class()


def mesh_longest_dimension(mesh):
    bounds = mesh.get_bounds()
    extent = bounds.box_extent
    return max(abs(extent.x) * 2.0, abs(extent.y) * 2.0, abs(extent.z) * 2.0)


def tune_weapon(path, target_length, location, rotation):
    bp, cls = generated_class(path)
    cdo = unreal.get_default_object(cls)
    first_static = cdo.get_editor_property("first_person_static_mesh")
    third_static = cdo.get_editor_property("third_person_static_mesh")
    mesh = first_static.get_static_mesh()
    if not mesh:
        raise RuntimeError(f"No static mesh assigned on {path}")

    length = mesh_longest_dimension(mesh)
    scale = target_length / length if length > 0 else 1.0
    scale_vec = unreal.Vector(scale, scale, scale)

    first_static.set_relative_location(unreal.Vector(*location), False, False)
    first_static.set_relative_rotation(unreal.Rotator(*rotation), False, False)
    first_static.set_relative_scale3d(scale_vec)

    third_static.set_relative_location(unreal.Vector(0.0, 0.0, 0.0), False, False)
    third_static.set_relative_rotation(unreal.Rotator(0.0, 0.0, 0.0), False, False)
    third_static.set_relative_scale3d(scale_vec)

    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    unreal.log(f"ZDH tuned {path}: imported_length={length:.2f}cm target={target_length:.2f}cm scale={scale:.5f}")


def main():
    # UE first person sockets vary by template, so this is a controlled first pass.
    # If the screenshot is close, we will tune these six values next.
    tune_weapon(
        SHOTGUN_BP_PATH,
        TARGET_SHOTGUN_LENGTH_CM,
        location=(12.0, 5.0, -7.0),
        rotation=(0.0, 90.0, 0.0),
    )
    tune_weapon(
        PISTOL_BP_PATH,
        TARGET_PISTOL_LENGTH_CM,
        location=(9.0, 3.0, -5.0),
        rotation=(0.0, 90.0, 0.0),
    )

    character_bp, character_cls = generated_class(CHARACTER_BP_PATH)
    character_cdo = unreal.get_default_object(character_cls)
    character_cdo.set_editor_property("default_weapon_classes", [generated_class(SHOTGUN_BP_PATH)[1]])
    unreal.EditorAssetLibrary.save_loaded_asset(character_bp)
    unreal.EditorAssetLibrary.save_directory("/Game/Items/Weapons", only_if_is_dirty=False, recursive=True)
    unreal.log("ZDH FPS weapon fitting pass 01 complete. Default weapon is shotgun only.")


main()
