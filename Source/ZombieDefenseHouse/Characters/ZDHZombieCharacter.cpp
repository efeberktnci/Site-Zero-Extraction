#include "ZDHZombieCharacter.h"

#include "../Components/ZDHHealthComponent.h"

AZDHZombieCharacter::AZDHZombieCharacter()
{
    bReplicates = true;
    HealthComponent = CreateDefaultSubobject<UZDHHealthComponent>(TEXT("HealthComponent"));
}
