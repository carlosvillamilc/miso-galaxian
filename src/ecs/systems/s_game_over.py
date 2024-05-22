from typing import Callable
import esper
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import show_game_over

def system_game_over(world: esper.World, game_over: dict, set_game_over: Callable, player_entity:int):
    if ServiceLocator.globals_service.player_lives < 0 and not game_over:
        show_game_over(world)
        ServiceLocator.sounds_service.play("assets/snd/game_over.ogg")
        set_game_over(True)
        world.delete_entity(player_entity)