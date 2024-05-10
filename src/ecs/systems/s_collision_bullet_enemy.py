import pygame
import esper

from src.create.prefab_creator import create_explosion
# from src.ecs.components.c_bullet_state import BulletStates, CBulletState
# from src.ecs.components.c_enemy_state import CEnemyState, EnemyStates
# from src.ecs.components.c_play_level_manager import CPlayLevelManager
# from src.ecs.components.c_player_state import CPlayerState, PlayerStates
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.engine.service_locator import ServiceLocator

def system_collision_bullet_enemy(world:esper.World):
    bullet_component = world.get_components(CTagBullet, CSurface, CTransform)
    enemy_component = world.get_components(CTagEnemy, CSurface, CTransform)
    for bullet_entity , (c_bullet_tag, c_bullet_surface, c_bullet_transform) in bullet_component:
        bullet_rect = c_bullet_surface.area.copy()
        bullet_rect.topleft = c_bullet_transform.pos.copy()
        for enemy_entity, (c_enemy_tag, c_enemy_surface, c_enemy_transform) in enemy_component:
            enemy_rect = c_enemy_surface.area.copy()
            enemy_rect.topleft = c_enemy_transform.pos.copy()
            if bullet_rect.colliderect(enemy_rect) and c_bullet_tag.type == 'player':
                ServiceLocator.globals_service.player_score += c_enemy_tag.score_value
                print('score_value',c_enemy_tag.score_value)
                if ServiceLocator.globals_service.player_score > ServiceLocator.globals_service.player_high_score:
                        ServiceLocator.globals_service.player_high_score = ServiceLocator.globals_service.player_score
                print('player_score',ServiceLocator.globals_service.player_score)
                print('player_high_score',ServiceLocator.globals_service.player_high_score)
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, c_enemy_transform.pos, 'enemy')