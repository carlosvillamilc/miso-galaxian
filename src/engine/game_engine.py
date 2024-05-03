import pygame
import esper
import json
import asyncio

class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        self.is_running = False
        self.ecs_world = esper.World

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
        pass

    def _calculate_time(self):
        pass

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        pass

    def _draw(self):
        pass

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
