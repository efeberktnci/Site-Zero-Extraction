#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "ZDHZombieCharacter.generated.h"

class UZDHHealthComponent;

UCLASS(Blueprintable)
class ZOMBIEDEFENSEHOUSE_API AZDHZombieCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AZDHZombieCharacter();

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ZDH|Components")
    TObjectPtr<UZDHHealthComponent> HealthComponent;

protected:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ZDH|Combat")
    float AttackDamage = 10.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "ZDH|Combat")
    float AttackRange = 120.0f;
};

