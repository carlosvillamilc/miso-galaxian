import pygame

# Scene
from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene
from src.create.prefab_creator import (create_title_logo, 
                                       create_background,
                                       create_press_start_game_text)

from src.ecs.systems.s_background import system_background
from src.ecs.systems.s_vertical_logo_movement import system_vertical_logo_movement
from src.ecs.systems.s_movement import system_movement

class MenuScene(Scene):
    def do_create(self):
        print("MenuScene created")
        create_background(self.ecs_world, self._game_engine.starfield_cfg)
        create_title_logo(self.ecs_world,self._game_engine.interface_cfg)
        create_press_start_game_text(self.ecs_world,self._game_engine.interface_cfg)


    def do_update(self, delta_time):
        #print("MenuScene updated")
        system_background(self.ecs_world, self._game_engine.screen, self._game_engine.delta_time)
        system_movement(self.ecs_world, delta_time)
        system_vertical_logo_movement(self.ecs_world)

    def do_action(self, action: CInputCommand):
        breakpoint()
        print("MenuScene action")

    def do_process_events(self, event: pygame.Event) -> None:
        # breakpoint()
        super().do_process_events(event)
        # Check if key space is pressed and switch to game scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            self.switch_scene("GAME_SCENE")
