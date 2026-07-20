import unreal


PATHS = [
    "/Game/Core",
    "/Game/Characters",
    "/Game/Characters/Player",
    "/Game/Characters/Zombies",
    "/Game/AI",
    "/Game/UI",
    "/Game/Items",
    "/Game/Maps",
    "/Game/Data",
    "/Game/Blueprints",
]


def main():
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    for path in PATHS:
        if not unreal.EditorAssetLibrary.does_directory_exist(path):
            unreal.EditorAssetLibrary.make_directory(path)
            unreal.log(f"Created content folder: {path}")
    unreal.EditorAssetLibrary.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    unreal.log("Zombie Defense House content skeleton is ready.")


main()

