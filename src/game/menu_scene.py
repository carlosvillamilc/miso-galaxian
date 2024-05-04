import pygame

# Scene
from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene


class MenuScene(Scene):
    def do_create(self):
        print("MenuScene created")

    def do_update(self, delta_time):
        print("MenuScene updated")

    def do_action(self, action: CInputCommand):
        print("MenuScene action")

    def do_process_events(self, event: pygame.Event) -> None:
        super().do_process_events(event)
        # Check if key space is pressed and switch to game scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_scene("GAME_SCENE")
