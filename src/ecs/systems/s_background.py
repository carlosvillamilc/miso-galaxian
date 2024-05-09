import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar

def system_background(ecs_world:esper.World, screen: pygame.Surface, delta_time:float):
    components = ecs_world.get_components(CTransform, CVelocity, CTagStar)
    screen_rect = screen.get_rect()
    for _, (c_t, c_v, _) in components:
        c_t.pos += c_v.vel * delta_time
        if (c_t.pos.y > screen_rect.height):
            c_t.pos.y = 0