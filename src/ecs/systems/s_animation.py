import esper
import pygame
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(ecs_world: esper.World, delta_time:float):
    components = ecs_world.get_components(CSurface, CAnimation)
    c_a: CAnimation
    c_s: CSurface
    for _, (c_s, c_a) in components:
        # 1. Disminuir el valor de current_time de la animacion
        c_a.current_animation_time -= delta_time
        # 2. Cuando current_time <=0, hacemos cambio de frame
        if c_a.current_animation_time <=0:
            #print(c_a.current_animation)
            #breakpoint()
            c_a.current_animation_time = c_a.animations_list[c_a.current_animation].framerate
            c_a.current_frame += 1
        # 3. Limitar el frame con sus propiendades de start y end
            if c_a.current_frame > c_a.animations_list[c_a.current_animation].end:
                c_a.current_frame = c_a.animations_list[c_a.current_animation].start
        # 4. Calcular la nueva sub area del rectangulo de sprite 
        rect_surf = c_s.surf.get_rect()
        c_s.area.width = rect_surf.width / c_a.number_frames
        c_s.area.x = c_s.area.width * c_a.current_frame