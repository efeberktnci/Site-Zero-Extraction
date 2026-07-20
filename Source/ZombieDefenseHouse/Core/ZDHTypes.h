#pragma once

#include "CoreMinimal.h"
#include "ZDHTypes.generated.h"

UENUM(BlueprintType)
enum class EZDHPlayerClass : uint8
{
    Assault,
    Medic,
    Engineer
};

UENUM(BlueprintType)
enum class EZDHTeam : uint8
{
    Players,
    Zombies
};

