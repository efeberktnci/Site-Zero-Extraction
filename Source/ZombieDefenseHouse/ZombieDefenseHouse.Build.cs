// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class ZombieDefenseHouse : ModuleRules
{
	public ZombieDefenseHouse(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"NetCore",
			"OnlineSubsystem",
			"OnlineSubsystemUtils",
			"GameplayAbilities",
			"GameplayTags",
			"GameplayTasks",
			"AIModule",
			"NavigationSystem",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"ZombieDefenseHouse",
			"ZombieDefenseHouse/Variant_Horror",
			"ZombieDefenseHouse/Variant_Horror/UI",
			"ZombieDefenseHouse/Variant_Shooter",
			"ZombieDefenseHouse/Variant_Shooter/AI",
			"ZombieDefenseHouse/Variant_Shooter/UI",
			"ZombieDefenseHouse/Variant_Shooter/Weapons"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
