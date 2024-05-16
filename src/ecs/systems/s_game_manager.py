import esper

from src.ecs.components.c_game_manager import CGameManager, PlayLevelState
from src.create.prefab_creator import create_all_enemies, create_player_bullet
from src.engine.service_locator import ServiceLocator

def system_game_manager(ecs_world:esper.World, c_game_manager:CGameManager, delta_time:float):
    if c_game_manager.state == PlayLevelState.START:
        c_game_manager.current_game_time += delta_time
        if c_game_manager.current_game_time > c_game_manager.start_game_time:
            create_all_enemies(ecs_world)            
            ecs_world.delete_entity(c_game_manager.start_game_entity)
            c_game_manager.state = PlayLevelState.PLAY           