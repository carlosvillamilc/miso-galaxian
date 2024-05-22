import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy, EnemyState
from src.ecs.components.tags.c_tag_enemy_ghost import CTagEnemyGhost
from src.engine.service_locator import ServiceLocator

def system_enemy_movement(world:esper.World):
    components = world.get_components(CSurface, CTransform, CVelocity, CTagEnemy)
    ghost_components = world.get_components(CVelocity, CTagEnemyGhost)
    window_cfg = ServiceLocator.configs_service.get("assets/cfg/window.json")

    c_s:CSurface
    c_t:CTransform
    c_v:CVelocity
    c_te:CTagEnemy
    c_vg:CVelocity
    for _, (c_s, c_t, c_v, c_te) in components:
        if c_te.state == EnemyState.MOVING:
            if c_t.pos.x <= 20 or (c_t.pos.x + c_s.area.size[0]) >= window_cfg["size"]["w"] - 20:
                for _, (c_s, c_t, c_v, _) in components:
                    c_v.vel.x = c_v.vel.x * -1

                for _, (c_vg, _) in ghost_components:
                    c_vg.vel.x = c_vg.vel.x * -1
                
                break