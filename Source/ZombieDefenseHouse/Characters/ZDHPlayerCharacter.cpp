#include "ZDHPlayerCharacter.h"

#include "../Components/ZDHHealthComponent.h"
#include "Net/UnrealNetwork.h"

AZDHPlayerCharacter::AZDHPlayerCharacter()
{
    bReplicates = true;
    HealthComponent = CreateDefaultSubobject<UZDHHealthComponent>(TEXT("HealthComponent"));
}

void AZDHPlayerCharacter::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(AZDHPlayerCharacter, PlayerClass);
    DOREPLIFETIME(AZDHPlayerCharacter, Infection);
}

void AZDHPlayerCharacter::SetPlayerClass(EZDHPlayerClass NewClass)
{
    if (HasAuthority())
    {
        PlayerClass = NewClass;
    }
}

void AZDHPlayerCharacter::AddInfection(float Amount)
{
    if (HasAuthority() && Amount > 0.0f)
    {
        Infection = FMath::Clamp(Infection + Amount, 0.0f, 100.0f);
    }
}
