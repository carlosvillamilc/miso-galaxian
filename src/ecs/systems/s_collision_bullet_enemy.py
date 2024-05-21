import esper

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet_player import CTagBulletPlayer
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_ghost import CTagEnemyGhost
from src.engine.service_locator import ServiceLocator

def system_collision_bullet_enemy(world: esper.World):
    bullet_component = world.get_components(CTagBulletPlayer, CSurface, CTransform)
    enemy_component = world.get_components(CTagEnemy, CSurface, CTransform)
    enemy_ghost_components = world.get_components(CTagEnemyGhost)
    for bullet_entity, (_, c_bullet_surface, c_bullet_transform) in bullet_component:
        bullet_rect = c_bullet_surface.area.copy()
        bullet_rect.topleft = c_bullet_transform.pos.copy()
        for enemy_entity, (
            c_enemy_tag,
            c_enemy_surface,
            c_enemy_transform,
        ) in enemy_component:
            enemy_rect = c_enemy_surface.area.copy()
            enemy_rect.topleft = c_enemy_transform.pos.copy()
            if bullet_rect.colliderect(enemy_rect):
                ServiceLocator.globals_service.player_score += c_enemy_tag.score_value
                for enemy_ghost_entity, (c_teg) in enemy_ghost_components:
                    if c_teg.index == c_enemy_tag.index:
                        world.delete_entity(enemy_ghost_entity)
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, c_enemy_transform.pos, "enemy")