import pygame
import esper
import json
import asyncio
from src.create.prefab_creator import create_background
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_background import system_background

class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_cfg.get('size').get('w'),
                                               self.window_cfg.get('size').get('h')),pygame.SCALED)
        self.is_running = False
        self.delta_time = 0
        self.framerate = self.window_cfg.get('framerate')
        self.clock = pygame.time.Clock()

        self.ecs_world = esper.World()

    def _load_config_files(self):
        path = './assets/cfg'
        with open(path + '/window.json', 'r', encoding='utf-8') as window_file:
            self.window_cfg = json.load(window_file)
        with open(path + '/interface.json', 'r') as interface_file:
            self.interface_cfg = json.load(interface_file)
        with open(path + '/starfield.json', 'r') as starfield_file:
            self.starfield_cfg = json.load(starfield_file)
        

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        create_background(self.ecs_world, self.starfield_cfg)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        pass

    def _update(self):
        system_background(self.ecs_world, self.screen, self.delta_time)

    def _draw(self):
        self.screen.fill((self.window_cfg.get('bg_color').get('r'),
                          self.window_cfg.get('bg_color').get('g'),
                          self.window_cfg.get('bg_color').get('b')))

        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
