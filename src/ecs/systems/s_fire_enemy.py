import esper
import random
from src.create.prefab_creator import create_enemy_bullet
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_fire_enemy(world:esper.World):
    components = world.get_components(CSurface, CTransform, CTagEnemy)

    c_s: CSurface
    c_t: CTransform
    for _,(c_s, c_t, _) in components:
        num_random = random.randint(0, 20000)

        if num_random > 1 and num_random < 10:
            create_enemy_bullet(world, c_t.pos, c_s.area.size)
            