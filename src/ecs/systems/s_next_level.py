import esper
import pygame
from typing import Callable
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator


def system_next_level(world: esper.World, run_next_level: Callable, delta_time: float):
    components = world.get_components(CTagEnemy)
    if len(components) == 0:
        run_next_level(delta_time)
        ServiceLocator.globals_service.current_level += 1
