#include "ZDHHealthComponent.h"

#include "Net/UnrealNetwork.h"

UZDHHealthComponent::UZDHHealthComponent()
{
    SetIsReplicatedByDefault(true);
}

void UZDHHealthComponent::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(UZDHHealthComponent, Health);
    DOREPLIFETIME(UZDHHealthComponent, MaxHealth);
}

void UZDHHealthComponent::ApplyDamage(float DamageAmount)
{
    if (!GetOwner() || !GetOwner()->HasAuthority() || DamageAmount <= 0.0f || IsDead())
    {
        return;
    }

    Health = FMath::Clamp(Health - DamageAmount, 0.0f, MaxHealth);
    BroadcastHealth();

    if (IsDead())
    {
        OnDeath.Broadcast();
    }
}

void UZDHHealthComponent::Heal(float HealAmount)
{
    if (!GetOwner() || !GetOwner()->HasAuthority() || HealAmount <= 0.0f || IsDead())
    {
        return;
    }

    Health = FMath::Clamp(Health + HealAmount, 0.0f, MaxHealth);
    BroadcastHealth();
}

void UZDHHealthComponent::OnRep_Health()
{
    BroadcastHealth();
}

void UZDHHealthComponent::BroadcastHealth()
{
    OnHealthChanged.Broadcast(Health, MaxHealth);
}
