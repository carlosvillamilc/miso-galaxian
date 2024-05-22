import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy, EnemyState
from src.ecs.components.tags.c_tag_enemy_ghost import CTagEnemyGhost
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator

def system_rendering_debug_velocity(world:esper.World, screen:pygame.Surface):
    fnt = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 6)
    debug_font:pygame.Surface = fnt.render("DEBUG_VIEW: VELOCITIES", False, pygame.Color(255, 0, 0))
    pos = pygame.Vector2(20, 10)
    screen.blit(debug_font, pos)

    components = world.get_components(CTransform, CVelocity)

    c_t:CTransform
    c_v:CVelocity
    for entity, (c_t, c_v) in components:
        is_a_star = world.has_component(entity, CTagStar)
        is_a_enemy_ghost = world.has_component(entity, CTagEnemyGhost)
        is_the_player = world.has_component(entity, CTagPlayer)
        if is_a_star or is_a_enemy_ghost or (c_v.vel.x == 0 and c_v.vel.y == 0 and not is_the_player):
            continue

        is_a_enemy = world.has_component(entity, CTagEnemy)
        enemy_component = None
        if is_a_enemy:
            enemy_component = world.component_for_entity(entity, CTagEnemy)

        if not is_a_enemy or enemy_component.state != EnemyState.MOVING:
            font_surf:pygame.Surface = fnt.render(str(c_v.vel), False, pygame.Color(255, 255, 255))
            pos = c_t.pos - pygame.Vector2(font_surf.get_size())
            screen.blit(font_surf, pos)