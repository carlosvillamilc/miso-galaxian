import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet_enemy import CTagBulletEnemy
from src.ecs.components.tags.c_tag_bullet_player import CTagBulletPlayer

def system_screen_bullet(ecs_world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = ecs_world.get_components(CTransform, CSurface, CTagBulletPlayer)
    components += ecs_world.get_components(CTransform, CSurface, CTagBulletEnemy)
    for bullet_entity, (c_t, c_s, _) in components:
        bullet_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if not screen_rect.contains(bullet_rect):
            ecs_world.delete_entity(bullet_entity)