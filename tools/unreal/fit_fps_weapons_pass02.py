import unreal

WEAPONS = [
    {
        "path": "/Game/Items/Weapons/Blueprints/BP_Weapon_G17",
        "target_length_cm": 18.5,
        "location": (9.0, 2.0, -3.0),
        "rotation": (0.0, 92.0, 0.0),
    },
    {
        "path": "/Game/Items/Weapons/Blueprints/BP_Weapon_PumpShotgun",
        "target_length_cm": 92.0,
        "location": (18.0, 4.0, -6.0),
        "rotation": (0.0, 92.0, 0.0),
    },
]
CHARACTER_BP_PATH = "/Game/Variant_Shooter/Blueprints/BP_ShooterCharacter"
DEFAULT_FIRST_WEAPON_PATH = "/Game/Items/Weapons/Blueprints/BP_Weapon_PumpShotgun"


def load_bp(path):
    bp = unreal.EditorAssetLibrary.load_asset(path)
    if not bp:
        raise RuntimeError(f"Could not load blueprint: {path}")
    return bp, bp.generated_class(), unreal.get_default_object(bp.generated_class())


def longest_dimension_cm(mesh):
    bounds = mesh.get_bounds()
    extent = bounds.box_extent
    return max(abs(extent.x) * 2.0, abs(extent.y) * 2.0, abs(extent.z) * 2.0)


def tune_weapon(spec):
    bp, cls, cdo = load_bp(spec["path"])
    first_static = cdo.get_editor_property("first_person_static_mesh")
    third_static = cdo.get_editor_property("third_person_static_mesh")
    mesh = first_static.get_static_mesh()
    if not mesh:
        raise RuntimeError(f"No static mesh assigned on {spec['path']}")

    imported_length = longest_dimension_cm(mesh)
    scale = spec["target_length_cm"] / imported_length if imported_length > 0.0 else 1.0

    first_static.set_relative_location(unreal.Vector(*spec["location"]), False, False)
    first_static.set_relative_rotation(unreal.Rotator(*spec["rotation"]), False, False)
    first_static.set_relative_scale3d(unreal.Vector(scale, scale, scale))

    third_static.set_relative_location(unreal.Vector(0.0, 0.0, 0.0), False, False)
    third_static.set_relative_rotation(unreal.Rotator(0.0, 0.0, 0.0), False, False)
    third_static.set_relative_scale3d(unreal.Vector(scale, scale, scale))

    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    unreal.log(f"ZDH tuned {spec['path']}: length={imported_length:.2f} target={spec['target_length_cm']:.2f} scale={scale:.6f}")
    return cls


def main():
    classes = []
    shotgun_class = None
    for spec in WEAPONS:
        cls = tune_weapon(spec)
        if spec["path"] == DEFAULT_FIRST_WEAPON_PATH:
            shotgun_class = cls
        classes.append(cls)

    character_bp, character_cls, character_cdo = load_bp(CHARACTER_BP_PATH)
    # Shotgun first, pistol second. Shift will swap to pistol.
    character_cdo.set_editor_property("default_weapon_classes", [shotgun_class] + [c for c in classes if c != shotgun_class])
    unreal.EditorAssetLibrary.save_loaded_asset(character_bp)
    unreal.EditorAssetLibrary.save_directory("/Game/Items/Weapons", only_if_is_dirty=False, recursive=True)
    unreal.log("ZDH FPS weapon fitting pass 02 complete. Shotgun first, pistol second.")


main()
