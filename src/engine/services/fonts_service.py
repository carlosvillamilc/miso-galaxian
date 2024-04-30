import pygame

class FontsService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, path:str):
        if path not in self._fonts:
            self._fonts[path] = pygame.font.Font(path)
        return self._fonts[path]