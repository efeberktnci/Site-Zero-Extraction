#include "ZDHGameMode.h"

#include "ZDHGameState.h"
#include "ZDHPlayerController.h"
#include "ZDHPlayerState.h"

AZDHGameMode::AZDHGameMode()
{
    GameStateClass = AZDHGameState::StaticClass();
    PlayerControllerClass = AZDHPlayerController::StaticClass();
    PlayerStateClass = AZDHPlayerState::StaticClass();
}
