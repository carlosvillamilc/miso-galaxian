import pygame
import esper
import random
from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy, EnemyState
from src.ecs.components.tags.c_tag_enemy_ghost import CTagEnemyGhost
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def system_enemy_steering(world:esper.World, player_entity:int, level:int, delta_time:float):
    components = world.get_components(CSurface, CTransform, CVelocity, CSteering, CTagEnemy)
    level_cfg = ServiceLocator.configs_service.get("assets/cfg/level_" + str(level) + ".json")
    window_cfg = ServiceLocator.configs_service.get("assets/cfg/window.json")
    p_t = world.component_for_entity(player_entity, CTransform)

    c_s:CSurface
    c_t:CTransform
    c_v:CVelocity
    c_se:CSteering
    c_te:CTagEnemy
    for _, (c_s, c_t, c_v, c_se, c_te) in components:
        num_random = random.randint(0, 50000)

        if (num_random > 1 and num_random < 10 and c_te.state != EnemyState.RETURNING) or c_te.state == EnemyState.STEERING:
            if c_te.state == EnemyState.MOVING:
                ServiceLocator.sounds_service.play("assets/snd/enemy_launch.ogg")

            c_te.state = EnemyState.STEERING
            goal_pos = pygame.Vector2(p_t.pos.x, window_cfg["size"]["h"])
            c_se.follow_vector = goal_pos - c_t.pos
            desired_good_length = level_cfg["follow_force"]
            c_se.follow_vector.scale_to_length(desired_good_length)
            c_v.vel = c_v.vel.lerp(c_se.follow_vector, delta_time * 5)

            if window_cfg["size"]["h"] - (c_t.pos.y + c_s.area.height) < 0.5:
                c_te.state = EnemyState.RETURNING
                c_t.pos = pygame.Vector2(c_t.pos.x, 0 - c_s.area.height)
        
        if c_te.state == EnemyState.RETURNING:
            ghost_components = world.get_components(CTransform, CVelocity, CTagEnemyGhost)

            c_tg:CTransform
            c_vg:CVelocity
            c_teg:CTagEnemyGhost
            for _, (c_tg, c_vg, c_teg) in ghost_components:
                if c_teg.index == c_te.index:
                    c_se.follow_vector = c_tg.pos - c_t.pos
                    desired_good_length = level_cfg["follow_force"]
                    c_se.follow_vector.scale_to_length(desired_good_length)
                    c_v.vel = c_v.vel.lerp(c_se.follow_vector, delta_time * 5)

                    if c_tg.pos.distance_to(c_t.pos) < 1:
                        c_t.pos = c_tg.pos.copy()
                        c_v.vel = c_vg.vel.copy()
                        c_te.state = EnemyState.MOVING