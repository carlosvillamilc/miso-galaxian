import esper
import pygame
from typing import Callable
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import show_next_level
from src.ecs.components.c_game_manager import GameState, CGameManager


def system_next_level(
    world: esper.World,
    run_next_level: Callable,
    delta_time: float,
    game_manager: CGameManager,
):
    components = world.get_components(CTagEnemy)
    if len(components) == 0 and game_manager.state == GameState.PLAY:
        show_next_level(world)
        run_next_level(delta_time)
