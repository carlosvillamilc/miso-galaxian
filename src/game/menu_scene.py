import pygame

# Scene
from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import (create_title_logo, 
                                       create_background,
                                       create_press_start_game_text)

from src.ecs.systems.s_background import system_background
from src.ecs.systems.s_vertical_logo_movement import system_vertical_logo_movement
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_blink import system_blink
class MenuScene(Scene):
    def do_create(self):
        print("MenuScene created")
        create_background(self.ecs_world, self._game_engine.starfield_cfg)
        create_title_logo(self.ecs_world,self._game_engine.interface_cfg)
        create_press_start_game_text(self.ecs_world,self._game_engine.interface_cfg)


    def do_update(self, delta_time):
        #print("MenuScene updated")
        system_background(self.ecs_world, self._game_engine.screen, self._game_engine.delta_time, self._game_engine.game_paused)
        system_movement(self.ecs_world, delta_time, self._game_engine.game_paused)
        system_vertical_logo_movement(self.ecs_world)
        system_blink(self.ecs_world, delta_time)

    def do_action(self, action: CInputCommand):
        breakpoint()
        print("MenuScene action")

    def do_process_events(self, event: pygame.Event) -> None:
        # breakpoint()
        super().do_process_events(event)
        # Check if key space is pressed and switch to game scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            ServiceLocator.sounds_service.play(self._game_engine.sounds_cfg["start_game"])
            self.switch_scene("GAME_SCENE")
            

