import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy, EnemyState
from src.ecs.components.tags.c_tag_enemy_ghost import CTagEnemyGhost
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator

def system_rendering_debug_rects(world:esper.World, screen:pygame.Surface):
    fnt = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 6)
    debug_font: pygame.Surface = fnt.render("DEBUG_VIEW: RECTS", False, pygame.Color(255, 0, 0))
    pos = pygame.Vector2(20, 10)
    screen.blit(debug_font, pos)

    components = world.get_components(CTransform, CSurface)

    c_t:CTransform
    c_s:CSurface
    for entity, (c_t, c_s) in components:
        is_a_star = world.has_component(entity, CTagStar)
        is_a_enemy_ghost = world.has_component(entity, CTagEnemyGhost)
        if not c_s.visible or is_a_star or is_a_enemy_ghost:
            continue

        final_rect = pygame.Rect(c_t.pos, c_s.area.size)
        pygame.draw.rect(screen, pygame.Color(10, 255, 10), final_rect, 1, 2)
        pygame.draw.circle(screen, pygame.Color(255, 255, 255), final_rect.topleft, 2, 2)

        is_a_enemy = world.has_component(entity, CTagEnemy)
        enemy_component = None
        if is_a_enemy:
            enemy_component = world.component_for_entity(entity, CTagEnemy)

        if not is_a_enemy or enemy_component.state != EnemyState.MOVING:
            pos_surf:pygame.Surface = fnt.render(str(c_t.pos), False, pygame.Color(255, 255, 255))
            size_surf:pygame.Surface = fnt.render(str(c_s.area.size), False, pygame.Color(255, 255, 0))
            pos = c_t.pos - pygame.Vector2(pos_surf.get_size())
            screen.blit(size_surf, pos)
            pos.y -= 10
            screen.blit(pos_surf, pos)