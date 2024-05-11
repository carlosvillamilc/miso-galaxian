import pygame

# Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import (create_title_logo, 
                                       create_background,
                                       create_press_start_game_text,
                                       create_menu_text)

from src.ecs.systems.s_background import system_background
from src.ecs.systems.s_vertical_logo_movement import system_vertical_logo_movement
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_blink import system_blink
class MenuScene(Scene):
    def do_create(self):
        print("MenuScene created")
        create_background(self.ecs_world)
        create_title_logo(self.ecs_world)
        create_press_start_game_text(self.ecs_world)
        create_menu_text(self.ecs_world)
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action, CInputCommand("START", pygame.K_z))


    def do_update(self, delta_time):
        #print("MenuScene updated")
        system_blink(self.ecs_world, delta_time)
        if ServiceLocator.globals_service.paused:
            return
        system_background(self.ecs_world, self._game_engine.screen, self._game_engine.delta_time)
        system_movement(self.ecs_world, delta_time)
        system_vertical_logo_movement(self.ecs_world)

    def do_action(self, action: CInputCommand):
        print("MenuScene action")
        if action.name == "START" and action.phase == CommandPhase.START:
            sounds_data = ServiceLocator.configs_service.get("assets/cfg/sounds.json")
            ServiceLocator.sounds_service.play(sounds_data["start_game"])
            self.switch_scene("GAME_SCENE")
        
    def do_process_events(self, event: pygame.Event) -> None:
        # breakpoint()
        super().do_process_events(event)
        # Check if key space is pressed and switch to game scene
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
        #     sounds_data = ServiceLocator.configs_service.get("assets/cfg/sounds.json")
        #     ServiceLocator.sounds_service.play(sounds_data["start_game"])
        #     self.switch_scene("GAME_SCENE")
            

