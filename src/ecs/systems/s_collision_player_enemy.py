import esper
import pygame
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_ghost import CTagEnemyGhost
from src.engine.service_locator import ServiceLocator


def system_collision_player_enemy(
    world: esper.World,
    player_entity: int,
    elapsed_time: float,
    player_explosion_time: float,
):
    time_difference = elapsed_time - player_explosion_time
    player_has_surface = world.has_component(player_entity, CSurface)

    if player_explosion_time == 0 or time_difference >= 3:
        player_data = ServiceLocator.configs_service.get("assets/cfg/player.json")
        p_t = world.component_for_entity(player_entity, CTransform)

        if not player_has_surface:
            p_t.pos = pygame.Vector2(
                player_data["start_point"]["x"], player_data["start_point"]["y"]
            )
            surface = ServiceLocator.images_service.get(player_data["image"])
            world.add_component(player_entity, CSurface.from_surface(surface))

        enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
        p_s = world.component_for_entity(player_entity, CSurface)
        p_t = world.component_for_entity(player_entity, CTransform)
        p_rect = CSurface.get_area_relative(p_s.area, p_t.pos)

        c_s: CSurface
        c_t: CTransform
        c_te: CTagEnemy
        for enemy_entity, (c_s, c_t, c_te) in enemy_components:
            enemy_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
            if enemy_rect.colliderect(p_rect):
                player_explosion_time = elapsed_time
                ServiceLocator.globals_service.player_score += c_te.score_value * 2
                ServiceLocator.globals_service.player_lives -= 1
                enemy_ghost_components = world.get_components(CTagEnemyGhost)

                c_teg: CTagEnemyGhost
                for enemy_ghost_entity, (c_teg) in enemy_ghost_components:
                    if c_teg.index == c_te.index:
                        world.delete_entity(enemy_ghost_entity)
                        break

                world.delete_entity(enemy_entity)
                create_explosion(
                    world, pygame.Vector2(p_t.pos.x - 10, p_t.pos.y - 10), "player"
                )
                create_explosion(world, c_t.pos, "enemy")

    elif time_difference < 3:
        if player_has_surface:
            world.remove_component(player_entity, CSurface)

    return player_explosion_time
