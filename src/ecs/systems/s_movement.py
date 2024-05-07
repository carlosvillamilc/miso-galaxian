import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar

def system_movement(ecs_world:esper.World, delta_time:float, paused: bool ):
    if paused:
        return
    components = ecs_world.get_components(CTransform, CVelocity)
    for ent, (c_t, c_v) in components:
        if ecs_world.has_component(ent, CTagStar):
            continue
        c_t.pos.x += c_v.vel.x * delta_time
        c_t.pos.y += c_v.vel.y * delta_time