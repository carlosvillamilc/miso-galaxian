import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_vertical_card import CVerticalCard
from src.ecs.components.c_velocity import CVelocity

def system_vertical_logo_movement(ecs_world:esper.World):
    components = ecs_world.get_components(CTransform, CVelocity, CVerticalCard)
    for ent, (c_tr, c_v, c_vc) in components:
        if not c_vc.started:
            c_vc.started = True
            c_tr.pos.y = c_vc.target_start_y
        else:
            c_v.vel.y = c_vc.speed
            if c_tr.pos.y <= c_vc.target_end_y:
                c_tr.pos.y = c_vc.target_end_y
                c_v.vel.y = 0
                ecs_world.remove_component(ent, CVerticalCard)