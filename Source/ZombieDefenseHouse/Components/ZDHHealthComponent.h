#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ZDHHealthComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FZDHHealthChangedSignature, float, NewHealth, float, MaxHealth);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FZDHDeathSignature);

UCLASS(ClassGroup=(ZDH), meta=(BlueprintSpawnableComponent))
class ZOMBIEDEFENSEHOUSE_API UZDHHealthComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UZDHHealthComponent();

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

    UFUNCTION(BlueprintCallable, Category = "ZDH|Health")
    void ApplyDamage(float DamageAmount);

    UFUNCTION(BlueprintCallable, Category = "ZDH|Health")
    void Heal(float HealAmount);

    UFUNCTION(BlueprintPure, Category = "ZDH|Health")
    float GetHealth() const { return Health; }

    UFUNCTION(BlueprintPure, Category = "ZDH|Health")
    float GetMaxHealth() const { return MaxHealth; }

    UFUNCTION(BlueprintPure, Category = "ZDH|Health")
    bool IsDead() const { return Health <= 0.0f; }

    UPROPERTY(BlueprintAssignable, Category = "ZDH|Health")
    FZDHHealthChangedSignature OnHealthChanged;

    UPROPERTY(BlueprintAssignable, Category = "ZDH|Health")
    FZDHDeathSignature OnDeath;

protected:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, ReplicatedUsing=OnRep_Health, Category = "ZDH|Health")
    float Health = 100.0f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Replicated, Category = "ZDH|Health")
    float MaxHealth = 100.0f;

    UFUNCTION()
    void OnRep_Health();

    void BroadcastHealth();
};

