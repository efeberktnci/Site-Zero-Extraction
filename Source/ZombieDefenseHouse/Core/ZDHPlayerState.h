#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerState.h"
#include "ZDHPlayerState.generated.h"

UCLASS()
class ZOMBIEDEFENSEHOUSE_API AZDHPlayerState : public APlayerState
{
    GENERATED_BODY()

public:
    AZDHPlayerState();

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

    UFUNCTION(BlueprintPure, Category = "ZDH|Stats")
    int32 GetZombieKills() const { return ZombieKills; }

    UFUNCTION(BlueprintPure, Category = "ZDH|Stats")
    int32 GetXP() const { return XP; }

    UFUNCTION(BlueprintPure, Category = "ZDH|Stats")
    int32 GetMoney() const { return Money; }

    UFUNCTION(BlueprintPure, Category = "ZDH|Stats")
    int32 GetMaterials() const { return Materials; }

protected:
    UPROPERTY(Replicated, BlueprintReadOnly, Category = "ZDH|Stats")
    int32 ZombieKills = 0;

    UPROPERTY(Replicated, BlueprintReadOnly, Category = "ZDH|Stats")
    int32 XP = 0;

    UPROPERTY(Replicated, BlueprintReadOnly, Category = "ZDH|Stats")
    int32 Money = 0;

    UPROPERTY(Replicated, BlueprintReadOnly, Category = "ZDH|Stats")
    int32 Materials = 0;
};

