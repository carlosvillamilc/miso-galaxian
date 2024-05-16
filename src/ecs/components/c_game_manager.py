from enum import Enum
from src.engine.service_locator import ServiceLocator

class PlayLevelState(Enum):
    START = 0
    PLAY = 1


class CGameManager:
    def __init__(self, start_game_entity) -> None:
        interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")

        self.state:PlayLevelState = PlayLevelState.START
        self.current_game_time = 0
        self.start_game_time = interface_data['game_start_text']['time']
        self.start_game_entity = start_game_entity