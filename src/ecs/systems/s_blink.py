import esper
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface

def system_blink(world:esper.World, delta_time:float):
    components = world.get_components(CBlink, CSurface)
    for _, (c_blk, c_s) in components:
        if not c_blk.enabled:
            continue
        c_blk.current_rate += delta_time
        if (c_blk.current_rate >= c_blk.rate):
            c_blk.current_rate = 0
            c_s.visible = not c_s.visible