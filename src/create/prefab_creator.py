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
from src.ecs.components.c_animation import CAnimation

from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def create_background(ecs_world: esper.World):
    background_data = ServiceLocator.configs_service.get("assets/cfg/starfield.json")
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

def create_square(ecs_world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    square_entity = ecs_world.create_entity()
    ecs_world.add_component(square_entity,
                        CSurface(size, col))
    ecs_world.add_component(square_entity,
                        CTransform(pos))
    ecs_world.add_component(square_entity,
                        CVelocity(vel))
    return square_entity

def create_title_logo(ecs_world:esper.World):
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    logo_data = interface_data["game_logo"]
    logo_surface = ServiceLocator.images_service.get(logo_data['image'])

    vel = pygame.Vector2(0,0)
    pos = pygame.Vector2(logo_data["pos"]["x"] - (logo_surface.get_width() / 2), 
                         logo_data["pos"]["y"])

    logo_entity = create_sprite(ecs_world, pos, vel, logo_surface)
    ecs_world.add_component(logo_entity, CVelocity(pygame.Vector2(0,0)))
    ecs_world.add_component(logo_entity, CVerticalCard(logo_data["logo_speed"], pos.y + logo_data["logo_offset"], pos.y))


def create_player(ecs_world: esper.World):
    player_data = ServiceLocator.configs_service.get("assets/cfg/player.json")
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
    player_surface = ecs_world.component_for_entity(player_entity, CSurface)
    return (player_entity, player_tr, player_v, player_tag, player_status, player_surface)


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


def create_player_bullet(ecs_world: esper.World, player_position: pygame.Vector2, player_size: pygame.Vector2):
    bullet_data = ServiceLocator.configs_service.get("assets/cfg/bullet.json")
    bullet_size = pygame.Vector2(bullet_data["size"]["w"], 
                          bullet_data["size"]["h"])
    position = pygame.Vector2(player_position.x + (player_size[0]/2) - (bullet_size[0]/2) , 
                              player_position.y + (player_size[1]/2) - (bullet_size[1]/2))
    

    vel = pygame.Vector2(bullet_data["velocity"]["x"],
                           bullet_data["velocity"]["y"])
    size = pygame.Vector2(bullet_data["size"]["w"], 
                          bullet_data["size"]["h"])
    color = pygame.Color(bullet_data["color"]["r"],
                         bullet_data["color"]["g"],
                         bullet_data["color"]["b"])
    
    bullet_entity = create_square(ecs_world, size, position, vel, color)
    
    ecs_world.add_component(bullet_entity, CTagBullet('player'))
    ServiceLocator.sounds_service.play(bullet_data["sound"])


def create_text(world:esper.World, text:str, font:pygame.font.Font, color:pygame.Color, pos:pygame.Vector2):
    text_entity = world.create_entity()
    world.add_component(text_entity,
                        CTransform(pos))
    world.add_component(text_entity,
                        CSurface.from_text(text, font, color))
    return text_entity

def create_press_start_game_text(ecs_world: esper.World) -> None:
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    title_text_data = interface_data["title_text"]
    title_text_color = pygame.color.Color(title_text_data["color"]["r"],
                                          title_text_data["color"]["g"],
                                          title_text_data["color"]["b"])    
    title_text_pos = pygame.Vector2(title_text_data["position"]["x"], title_text_data["position"]["y"])
    title_text_font = ServiceLocator.fonts_service.get(interface_data["font"], title_text_data["size"])

    start_text = create_text(ecs_world, 
                             title_text_data["text"], 
                             title_text_font,
                             title_text_color, 
                             title_text_pos)
    
    blink_rate = title_text_data["blink_rate"]
    ecs_world.add_component(start_text, CBlink(blink_rate))
    ecs_world.add_component(start_text, CVelocity(pygame.Vector2(0,0)))
    ecs_world.add_component(start_text, CVerticalCard(interface_data["game_logo"]["logo_speed"], 
                                                      title_text_pos.y + interface_data["game_logo"]["logo_offset"], 
                                                      title_text_pos.y))
    

def create_paused_text(ecs_world:esper.World):
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    pause_text_data = interface_data["pause_text"]
    font = ServiceLocator.fonts_service.get(interface_data["font"], 
                                            pause_text_data["size"])
    color = pygame.Color(pause_text_data["color"]["r"],
                         pause_text_data["color"]["g"],
                         pause_text_data["color"]["b"])
    blink_rate = pause_text_data["blink_rate"]
    position = pygame.Vector2(pause_text_data["position"]["x"], pause_text_data["position"]["y"])
    text = pause_text_data["text"]
    pause_text = create_text(ecs_world, text, font, color, position)
    ecs_world.add_component(pause_text, CBlink(blink_rate))
    return pause_text 


def create_game_start_text(ecs_world:esper.World) -> int:
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    game_start_text_data = interface_data["game_start_text"]
    font = ServiceLocator.fonts_service.get(interface_data["font"], 
                                            game_start_text_data["size"])
    color = pygame.Color(game_start_text_data["color"]["r"],
                         game_start_text_data["color"]["g"],
                         game_start_text_data["color"]["b"])
    position = pygame.Vector2(game_start_text_data["position"]["x"], game_start_text_data["position"]["y"])
    text = game_start_text_data["text"]
    game_start_text = create_text(ecs_world, text, font, color, position)

    return game_start_text    

def create_explosion(ecs_world: esper.World, pos: pygame.Vector2, type:str):
    explosion_data = ServiceLocator.configs_service.get("assets/cfg/explosions.json")
    explosion_data = explosion_data[type]
    explosion_surface = ServiceLocator.images_service.get(explosion_data['image'])

    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(ecs_world, pos, vel, explosion_surface)
    ecs_world.add_component(explosion_entity, CTagExplosion())
    ecs_world.add_component(explosion_entity, CAnimation(explosion_data["animations"]))
    ServiceLocator.sounds_service.play(explosion_data["sound"])
    return explosion_entity

def create_enemy(ecs_world: esper.World,
                 pos: pygame.Vector2,
                 velocity: pygame.Vector2,
                 score_value:float,
                 image_path: str,
                 animations:dict) -> None:
    image = ServiceLocator.images_service.get(image_path)
    enemy_entity = create_sprite(ecs_world, pos, velocity, image)
    ecs_world.add_component(enemy_entity, CTagEnemy(score_value))
    ecs_world.add_component(enemy_entity, CAnimation(animations))


def create_all_enemies(ecs_world: esper.World):
    enemies_data = ServiceLocator.configs_service.get("assets/cfg/enemies.json")
    
    separate_y = 14  
    separate_x = 18
    
    enemy_fourth_line_config = enemies_data["enemy_04"]
    enemy_third_line_config = enemies_data["enemy_03"]
    enemy_second_line_config = enemies_data["enemy_02"]
    enemy_first_line_config = enemies_data["enemy_01"]
    speed = pygame.Vector2(0, 0)

    start_pos: pygame.Vector2 = pygame.Vector2(42, 80)
    score_value = enemy_first_line_config["score_value"]
    image = enemy_first_line_config["image"]
    animations = enemy_first_line_config["animations"]
    for y in range(3):
        for x in range(10):
            pos = pygame.Vector2(start_pos.x + separate_x * x, start_pos.y + separate_y * y)
            print(pos)
            create_enemy(ecs_world, pos, speed, score_value, image, animations)

    start_pos.x = 58
    start_pos.y -= separate_y
    score_value = enemy_second_line_config["score_value"]
    image = enemy_second_line_config["image"]
    animations = enemy_second_line_config["animations"]
    for x in range(8):
        pos = pygame.Vector2(start_pos.x + separate_x * x, start_pos.y)
        print(pos)
        create_enemy(ecs_world, pos, speed, score_value, image, animations)

    start_pos.x += separate_x
    start_pos.y -= separate_y
    score_value = enemy_third_line_config["score_value"]
    image = enemy_third_line_config["image"]
    animations = enemy_third_line_config["animations"]
    for x in range(6):
        pos = pygame.Vector2(start_pos.x + separate_x * x, start_pos.y)
        create_enemy(ecs_world, pos, speed, score_value, image, animations)

    start_pos.x += separate_x - 1
    start_pos.y -= separate_y + 1
    score_value = enemy_fourth_line_config["score_value"]
    image = enemy_fourth_line_config["image"]
    animations = enemy_fourth_line_config["animations"]
    for x in range(2):        
        pos = pygame.Vector2(start_pos.x + separate_x * 3 * x, start_pos.y)
        create_enemy(ecs_world, pos, speed, score_value, image, animations)


def create_enemy_bullet(ecs_world:esper.World, pos:pygame.Vector2, vel_x:float):
    bullet_cfg = ServiceLocator.configs_service.get("assets/cfg/bullets.json")
    enemy_bullet_cfg = bullet_cfg["enemy"]
    size = pygame.Vector2(enemy_bullet_cfg["size"]["w"], 
                          enemy_bullet_cfg["size"]["h"])
    vel = pygame.Vector2(enemy_bullet_cfg["velocity"]["x"], enemy_bullet_cfg["velocity"]["y"])
    color = pygame.Color(enemy_bullet_cfg["color"]["r"], 
                           enemy_bullet_cfg["color"]["g"],
                           enemy_bullet_cfg["color"]["b"])
    enemy_bullet_entity = create_square(ecs_world, size, pos, vel, color)
        
    ecs_world.add_component(enemy_bullet_entity,
                        CTagBullet("enemy"))