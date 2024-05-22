import pygame
import esper

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet_enemy import CTagBulletEnemy
from src.engine.service_locator import ServiceLocator

def system_collision_bullet_player(ecs_world:esper.World, player_entity:int, elapsed_time:float, player_explosion_time:float):
    time_difference = elapsed_time - player_explosion_time
    player_has_surface = ecs_world.has_component(player_entity, CSurface)

    if player_explosion_time == 0 or time_difference >= 3:
        player_data = ServiceLocator.configs_service.get("assets/cfg/player.json")
        p_t = ecs_world.component_for_entity(player_entity, CTransform)

        if not player_has_surface:
            p_t.pos = pygame.Vector2(player_data["start_point"]["x"], player_data["start_point"]["y"])
            surface = ServiceLocator.images_service.get(player_data["image"])
            ecs_world.add_component(player_entity, CSurface.from_surface(surface))
        
        bullet_component = ecs_world.get_components(CTagBulletEnemy, CSurface, CTransform)
        p_s = ecs_world.component_for_entity(player_entity, CSurface)
        p_rect = CSurface.get_area_relative(p_s.area, p_t.pos)

        c_bullet_surface:CSurface
        c_bullet_transform:CTransform
        for bullet_entity, (_, c_bullet_surface, c_bullet_transform) in bullet_component:
            bullet_rect = CSurface.get_area_relative(c_bullet_surface.area, c_bullet_transform.pos)
            if bullet_rect.colliderect(p_rect):
                player_explosion_time = elapsed_time
                ecs_world.delete_entity(bullet_entity)
                create_explosion(ecs_world, pygame.Vector2(p_t.pos.x - 10, p_t.pos.y - 10), "player")
                ServiceLocator.globals_service.player_lives -= 1

    elif time_difference < 3:
        if player_has_surface:
            ecs_world.remove_component(player_entity, CSurface)

    return player_explosion_time