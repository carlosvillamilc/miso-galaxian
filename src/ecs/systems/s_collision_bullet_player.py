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

def system_collision_bullet_player(ecs_world:esper.World):
    bullet_component = ecs_world.get_components(CTagBullet, CSurface, CTransform)
    player_component = ecs_world.get_components(CSurface, CTransform)

    for bullet_entity, (c_bullet_tag, c_bullet_surface, c_bullet_transform) in bullet_component:
        bullet_rect = c_bullet_surface.area.copy()
        bullet_rect.topleft = c_bullet_transform.pos.copy()

        for player_entity, (c_player_surface, c_player_transform) in player_component:
            player_rect = c_player_surface.area.copy()
            player_rect.topleft = c_player_transform.pos.copy()
            if bullet_rect.colliderect(player_rect) and c_bullet_tag.type == "enemy":
                ecs_world.delete_entity(bullet_entity)
                player_pos = c_player_transform.pos.copy() - pygame.Vector2(c_player_surface.area.centerx, c_player_surface.area.centery)
                create_explosion(ecs_world, player_pos, "player")
           
