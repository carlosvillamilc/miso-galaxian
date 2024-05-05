import pygame
import esper
import random

from src.engine.service_locator import ServiceLocator

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity 
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_vertical_card import CVerticalCard
from src.ecs.components.c_player_status import CPlayerStatus
from src.ecs.components.c_input_command import CInputCommand

from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet

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

def create_sprite(ecs_world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity,
                        CTransform(pos))
    ecs_world.add_component(sprite_entity,
                        CVelocity(vel))
    ecs_world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity

def create_title_logo(ecs_world:esper.World, interface_data: dict):
    logo_data = interface_data["game_logo"]
    logo_surface = ServiceLocator.images_service.get(logo_data['image'])

    vel = pygame.Vector2(0,0)
    pos = pygame.Vector2(logo_data["pos"]["x"] - (logo_surface.get_width() / 2), 
                         logo_data["pos"]["y"])

    logo_entity = create_sprite(ecs_world, pos, vel, logo_surface)
    ecs_world.add_component(logo_entity, CVelocity(pygame.Vector2(0,0)))
    ecs_world.add_component(logo_entity, CVerticalCard(logo_data["logo_speed"], pos.y + logo_data["logo_offset"], pos.y))


def create_player(ecs_world: esper.World, player_data: dict):
    #player_config = ServiceLocator.images_service.get("assets/cfg/player.json")
    surface = ServiceLocator.images_service.get(player_data["image"])
    pos = pygame.Vector2(player_data["start_point"]["x"],  
                         player_data["start_point"]["y"])
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(ecs_world, pos, vel, surface)
    ecs_world.add_component(player_entity, CTagPlayer(player_data["input_speed"]))
    ecs_world.add_component(player_entity, CPlayerStatus(player_data["lives"]))
    player_tr = ecs_world.component_for_entity(player_entity, CTransform)
    player_v = ecs_world.component_for_entity(player_entity, CVelocity)
    player_tag = ecs_world.component_for_entity(player_entity, CTagPlayer)
    player_status = ecs_world.component_for_entity(player_entity, CPlayerStatus)
    return (player_entity, player_tr, player_v, player_tag, player_status)


def create_input_player(ecs_world: esper.World):
    # keyboard
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    pause_game = ecs_world.create_entity()
    # mouse
    input_fire = ecs_world.create_entity()   

    ecs_world.add_component(input_left, CInputCommand('PLAYER_LEFT', pygame.K_LEFT))
    ecs_world.add_component(input_right, CInputCommand('PLAYER_RIGHT', pygame.K_RIGHT))  
    ecs_world.add_component(input_fire, CInputCommand('PLAYER_FIRE', pygame.K_z))
    ecs_world.add_component(pause_game, CInputCommand("PAUSE_GAME", pygame.K_p))


def create_bullet(ecs_world: esper.World, mouse_position: pygame.Vector2, player_position: pygame.Vector2, player_size: pygame.Vector2,bullet_data: dict):
    bullet_surface = ServiceLocator.images_service.get(bullet_data['image'])
    bullet_size = bullet_surface.get_rect().size

    position = pygame.Vector2(player_position.x + (player_size[0]/2) - (bullet_size[0]/2) , 
                              player_position.y + (player_size[1]/2) - (bullet_size[1]/2))
    
    direction = (mouse_position - player_position).normalize()
    
    vel = direction * bullet_data["velocity"]

    bullet_entity = create_sprite(ecs_world,position,vel,bullet_surface)
    ecs_world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_data["sound"])