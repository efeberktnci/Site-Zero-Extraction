#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ZDHBarricade.generated.h"

UCLASS(Blueprintable)
class ZOMBIEDEFENSEHOUSE_API AZDHBarricade : public AActor
{
    GENERATED_BODY()

public:
    AZDHBarricade();

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

    UFUNCTION(BlueprintCallable, Category = "ZDH|Barricade")
    void ApplyBarricadeDamage(float DamageAmount);

    UFUNCTION(BlueprintCallable, Category = "ZDH|Barricade")
    void RepairBarricade(float RepairAmount);

    UFUNCTION(BlueprintPure, Category = "ZDH|Barricade")
    float GetHealthPercent() const;

protected:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Replicated, Category = "ZDH|Barricade")
    float Health = 100.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Replicated, Category = "ZDH|Barricade")
    float MaxHealth = 100.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ZDH|Barricade")
    int32 RepairMaterialCost = 1;
};

