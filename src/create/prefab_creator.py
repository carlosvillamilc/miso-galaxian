import pygame
import esper
import random
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity 
from src.ecs.components.c_blink import CBlink
from src.ecs.components.tags.c_tag_star import CTagStar
def create_background(ecs_world: esper.World, background_data: dict):
    number_of_stars = background_data["number_of_stars"]
    speed_range = (background_data["vertical_speed"]["min"], background_data["vertical_speed"]["max"])
    blink_rate_range = (background_data["blink_rate"]["min"], background_data["blink_rate"]["max"])
    star_colors = background_data["star_colors"]
    for _ in range(number_of_stars):
        star_entity = ecs_world.create_entity()

        size = pygame.Vector2(1, 1)
        color_choice = random.choice(star_colors)
        color = pygame.color.Color(color_choice["r"], color_choice["g"], color_choice["b"])

        pos = pygame.Vector2(random.randint(10, 246), random.randint(10, 230))
        vertical_speed = random.randint(speed_range[0], speed_range[1])
        vel = pygame.Vector2(0, vertical_speed)

        blink_rate = random.uniform(blink_rate_range[0], blink_rate_range[1])
        current_blink_rate = random.uniform(blink_rate_range[0], blink_rate_range[1])
        ecs_world.add_component(star_entity, CSurface(size, color))
        ecs_world.add_component(star_entity, CTransform(pos))
        ecs_world.add_component(star_entity, CVelocity(vel))
        ecs_world.add_component(star_entity, CBlink(blink_rate, current_blink_rate))
        ecs_world.add_component(star_entity, CTagStar())