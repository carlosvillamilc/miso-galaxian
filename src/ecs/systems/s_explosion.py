import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_explosion(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)
    for explosion_entity,  (c_a, _) in components:
        if c_a.current_frame == c_a.animations_list[c_a.current_animation].end:
            world.delete_entity(explosion_entity)
