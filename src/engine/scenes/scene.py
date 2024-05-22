import pygame
import esper
import src.engine.game_engine

# Systems
from src.ecs.systems.s_input import system_input
from src.ecs.systems.s_rendering import system_rendering

# Components
from src.ecs.components.c_input_command import CInputCommand

class Scene:
    def __init__(self, game_engine: "src.engine.game_engine.GameEngine") -> None:
        self.ecs_world: esper.World = esper.World()
        self._game_engine: "src.engine.game_engine.GameEngine" = game_engine
        self.screen_rect = self._game_engine.screen.get_rect()

    def do_process_events(self, event: pygame.event.Event) -> None:
        system_input(self.ecs_world, event, self.do_action)

    def simulate(self, delta_time, elapsed_time):
        self.do_update(delta_time, elapsed_time)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self._do_clean()

    def switch_scene(self, scene_name: str) -> None:
        self._game_engine.switch_scene(scene_name)

    def do_create(self):
        pass

    def do_update(self, delta_time, elapsed_time):
        pass

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)

    def do_action(self, action: CInputCommand):
        pass

    def _do_clean(self):
        pass