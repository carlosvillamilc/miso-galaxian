import pygame

# Scene
from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene


class GameScene(Scene):
    def do_create(self):
        print("GameScene created")

    def do_update(self, delta_time):
        print("GameScene updated")

    def do_action(self, action: CInputCommand):
        print("GameScene action")

    def do_process_events(self, event: pygame.Event) -> None:
        super().do_process_events(event)
        # Check if key space is pressed and switch to manu scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_scene("MENU_SCENE")
