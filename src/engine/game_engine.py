import pygame
import esper
import json
import asyncio

# Prefabs
from src.create.prefab_creator import create_background

# Scenes
from src.engine.scenes.scene import Scene
from src.game.menu_scene import MenuScene
from src.game.game_scene import GameScene

# Systems
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_background import system_background

# Components
from src.ecs.components.c_input_command import CInputCommand


class GameEngine:
    def __init__(self) -> None:
        self.starfield_cfg = None
        self._load_config_files()

        pygame.init()
        self.screen = pygame.display.set_mode(
            (
                self.window_cfg.get("size").get("w"),
                self.window_cfg.get("size").get("h"),
            ),
            pygame.SCALED,
        )
        self.is_running = False

        self._scenes: dict[str, Scene] = {}
        self._scenes["MENU_SCENE"] = MenuScene(self)
        self._scenes["GAME_SCENE"] = GameScene(self)
        self._current_scene: Scene = None
        self._scene_name_to_switch: str = None

        self.delta_time = 0
        self.framerate = self.window_cfg.get("framerate")
        self.clock = pygame.time.Clock()

        self.ecs_world = esper.World()

    def _load_config_files(self):
        path = "./assets/cfg"
        with open(path + "/window.json", "r", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open(path + "/interface.json", "r") as interface_file:
            self.interface_cfg = json.load(interface_file)
        with open(path + "/starfield.json", "r") as starfield_file:
            self.starfield_cfg = json.load(starfield_file)
        with open(path + "/player.json", "r") as player_file:
            self.player_cfg = json.load(player_file)
        with open(path + "/bullet.json", "r") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)

    async def run(self, start_scene_name: str) -> None:
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            await asyncio.sleep(0)
        self._clean()

    def switch_scene(self, scene_name: str) -> None:
        self._scene_name_to_switch = scene_name

    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self.delta_time)

    def _draw(self):
        self.screen.fill(
            (
                self.window_cfg.get("bg_color").get("r"),
                self.window_cfg.get("bg_color").get("g"),
                self.window_cfg.get("bg_color").get("b"),
            )
        )
        system_rendering(self.ecs_world, self.screen)
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, action: CInputCommand):
        self._current_scene.do_action(action)

    def _do_clean(self):
        if self._current_scene:
            self._current_scene.clean()
        pygame.quit()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
