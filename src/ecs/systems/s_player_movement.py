import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_movement(world: esper.World, screen: pygame.Surface, paused: bool):
    if paused:
        return
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagPlayer)
    for _, (c_t, c_s, _) in components:
        c_t.pos.x = max(screen_rect.left + 20, min(c_t.pos.x, screen_rect.right - 20 - c_s.area.width))
        