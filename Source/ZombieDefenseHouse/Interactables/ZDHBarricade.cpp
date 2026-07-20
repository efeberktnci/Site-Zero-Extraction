#include "ZDHBarricade.h"

#include "Net/UnrealNetwork.h"

AZDHBarricade::AZDHBarricade()
{
    bReplicates = true;
}

void AZDHBarricade::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(AZDHBarricade, Health);
    DOREPLIFETIME(AZDHBarricade, MaxHealth);
}

void AZDHBarricade::ApplyBarricadeDamage(float DamageAmount)
{
    if (HasAuthority() && DamageAmount > 0.0f)
    {
        Health = FMath::Clamp(Health - DamageAmount, 0.0f, MaxHealth);
    }
}

void AZDHBarricade::RepairBarricade(float RepairAmount)
{
    if (HasAuthority() && RepairAmount > 0.0f)
    {
        Health = FMath::Clamp(Health + RepairAmount, 0.0f, MaxHealth);
    }
}

float AZDHBarricade::GetHealthPercent() const
{
    return MaxHealth > 0.0f ? Health / MaxHealth : 0.0f;
}
