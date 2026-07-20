import os
import unreal


PROJECT_ROOT = r"D:/Unreal Projects/ZombieDefenseHouse"
PISTOL_SOURCE = os.path.join(PROJECT_ROOT, "SourceAssets/Weapons/WPN_Pistol_G17_Source.glb")
SHOTGUN_SOURCE = os.path.join(PROJECT_ROOT, "SourceAssets/Weapons/WPN_Shotgun_Pump_Source.glb")

MODEL_DIR = "/Game/Items/Weapons/Models"
BLUEPRINT_DIR = "/Game/Items/Weapons/Blueprints"


def make_dir(path):
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)


def import_glb(source_file, destination_name):
    make_dir(MODEL_DIR)

    task = unreal.AssetImportTask()
    task.filename = source_file
    task.destination_path = MODEL_DIR
    task.destination_name = destination_name
    task.automated = True
    task.save = True
    task.replace_existing = True

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

    imported_paths = list(task.imported_object_paths)
    unreal.log(f"Imported {source_file}: {imported_paths}")
    return imported_paths


def find_first_static_mesh(asset_paths):
    for path in asset_paths:
        asset = unreal.EditorAssetLibrary.load_asset(path)
        if isinstance(asset, unreal.StaticMesh):
            return asset

    # Interchange may import nested/generated assets with a prefix; search the model folder.
    for path in unreal.EditorAssetLibrary.list_assets(MODEL_DIR, recursive=True):
        asset = unreal.EditorAssetLibrary.load_asset(path)
        if isinstance(asset, unreal.StaticMesh):
            return asset

    return None


def duplicate_weapon(template_path, target_name):
    make_dir(BLUEPRINT_DIR)
    target_path = f"{BLUEPRINT_DIR}/{target_name}"

    if unreal.EditorAssetLibrary.does_asset_exist(target_path):
        unreal.EditorAssetLibrary.delete_asset(target_path)

    if not unreal.EditorAssetLibrary.duplicate_asset(template_path, target_path):
        raise RuntimeError(f"Could not duplicate {template_path} to {target_path}")

    return unreal.EditorAssetLibrary.load_asset(target_path)


def configure_weapon_blueprint(blueprint_asset, static_mesh, first_person_location, first_person_rotation, first_person_scale):
    generated_class = blueprint_asset.generated_class()
    default_object = unreal.get_default_object(generated_class)

    first_static = default_object.get_editor_property("first_person_static_mesh")
    third_static = default_object.get_editor_property("third_person_static_mesh")

    first_static.set_static_mesh(static_mesh)
    third_static.set_static_mesh(static_mesh)

    first_static.set_relative_location(unreal.Vector(*first_person_location), False, False)
    first_static.set_relative_rotation(unreal.Rotator(*first_person_rotation), False, False)
    first_static.set_relative_scale3d(unreal.Vector(*first_person_scale))

    third_static.set_relative_location(unreal.Vector(0.0, 0.0, 0.0), False, False)
    third_static.set_relative_rotation(unreal.Rotator(0.0, 0.0, 0.0), False, False)
    third_static.set_relative_scale3d(unreal.Vector(1.0, 1.0, 1.0))

    unreal.EditorAssetLibrary.save_loaded_asset(blueprint_asset)


def main():
    pistol_paths = import_glb(PISTOL_SOURCE, "SM_WPN_G17")
    shotgun_paths = import_glb(SHOTGUN_SOURCE, "SM_WPN_PumpShotgun")

    pistol_mesh = find_first_static_mesh(pistol_paths)
    shotgun_mesh = find_first_static_mesh(shotgun_paths)

    if not pistol_mesh:
        raise RuntimeError("Could not find imported pistol static mesh.")
    if not shotgun_mesh:
        raise RuntimeError("Could not find imported shotgun static mesh.")

    pistol_bp = duplicate_weapon(
        "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Pistol",
        "BP_Weapon_G17",
    )
    shotgun_bp = duplicate_weapon(
        "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Rifle",
        "BP_Weapon_PumpShotgun",
    )

    # These are first-pass FPS offsets. We will tune in-editor after seeing the result.
    configure_weapon_blueprint(
        pistol_bp,
        pistol_mesh,
        first_person_location=(0.0, 0.0, 0.0),
        first_person_rotation=(0.0, 0.0, 0.0),
        first_person_scale=(1.0, 1.0, 1.0),
    )
    configure_weapon_blueprint(
        shotgun_bp,
        shotgun_mesh,
        first_person_location=(0.0, 0.0, 0.0),
        first_person_rotation=(0.0, 0.0, 0.0),
        first_person_scale=(1.0, 1.0, 1.0),
    )

    unreal.EditorAssetLibrary.save_directory("/Game/Items/Weapons", only_if_is_dirty=False, recursive=True)
    unreal.log("ZDH weapon assets imported and weapon blueprints created.")


main()
