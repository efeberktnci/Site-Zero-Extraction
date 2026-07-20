#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "../Core/ZDHTypes.h"
#include "ZDHPlayerCharacter.generated.h"

class UZDHHealthComponent;

UCLASS(Blueprintable)
class ZOMBIEDEFENSEHOUSE_API AZDHPlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AZDHPlayerCharacter();

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

    UFUNCTION(BlueprintPure, Category = "ZDH|Class")
    EZDHPlayerClass GetPlayerClass() const { return PlayerClass; }

    UFUNCTION(BlueprintCallable, Category = "ZDH|Class")
    void SetPlayerClass(EZDHPlayerClass NewClass);

    UFUNCTION(BlueprintPure, Category = "ZDH|Infection")
    float GetInfection() const { return Infection; }

    UFUNCTION(BlueprintCallable, Category = "ZDH|Infection")
    void AddInfection(float Amount);

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ZDH|Components")
    TObjectPtr<UZDHHealthComponent> HealthComponent;

protected:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Replicated, Category = "ZDH|Class")
    EZDHPlayerClass PlayerClass = EZDHPlayerClass::Assault;

    UPROPERTY(BlueprintReadOnly, Replicated, Category = "ZDH|Infection")
    float Infection = 0.0f;
};
