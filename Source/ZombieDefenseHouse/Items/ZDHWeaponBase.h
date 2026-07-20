#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ZDHWeaponBase.generated.h"

UCLASS(Blueprintable)
class ZOMBIEDEFENSEHOUSE_API AZDHWeaponBase : public AActor
{
    GENERATED_BODY()

public:
    AZDHWeaponBase();

protected:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ZDH|Weapon")
    float Damage = 25.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ZDH|Weapon")
    int32 MagazineSize = 12;

    UPROPERTY(BlueprintReadOnly, Category = "ZDH|Weapon")
    int32 CurrentAmmo = 12;
};

