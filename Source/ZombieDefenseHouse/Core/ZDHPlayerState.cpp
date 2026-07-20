#include "ZDHPlayerState.h"

#include "Net/UnrealNetwork.h"

AZDHPlayerState::AZDHPlayerState()
{
    bReplicates = true;
}

void AZDHPlayerState::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(AZDHPlayerState, ZombieKills);
    DOREPLIFETIME(AZDHPlayerState, XP);
    DOREPLIFETIME(AZDHPlayerState, Money);
    DOREPLIFETIME(AZDHPlayerState, Materials);
}
