import unreal


CHARACTER_BP_PATH = "/Game/Variant_Shooter/Blueprints/BP_ShooterCharacter"
PISTOL_BP_PATH = "/Game/Items/Weapons/Blueprints/BP_Weapon_G17"
SHOTGUN_BP_PATH = "/Game/Items/Weapons/Blueprints/BP_Weapon_PumpShotgun"


def load_generated_class(path):
    blueprint = unreal.EditorAssetLibrary.load_asset(path)
    if not blueprint:
        raise RuntimeError(f"Could not load blueprint: {path}")
    return blueprint.generated_class()


def main():
    character_bp = unreal.EditorAssetLibrary.load_asset(CHARACTER_BP_PATH)
    if not character_bp:
        raise RuntimeError(f"Could not load character blueprint: {CHARACTER_BP_PATH}")

    default_object = unreal.get_default_object(character_bp.generated_class())
    default_object.set_editor_property(
        "default_weapon_classes",
        [
            load_generated_class(SHOTGUN_BP_PATH),
            load_generated_class(PISTOL_BP_PATH),
        ],
    )

    unreal.EditorAssetLibrary.save_loaded_asset(character_bp)
    unreal.log("ZDH default first-person weapons configured.")


main()
