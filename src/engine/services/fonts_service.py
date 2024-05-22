import pygame

class FontsService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, path:str, size:int):
        if path not in self._fonts:
            self._fonts[(path, size)] = pygame.font.Font(path, size)
        return self._fonts[(path, size)]