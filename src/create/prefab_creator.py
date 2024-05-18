import pygame
import esper
import random

from src.create.utils import convert_double_digit
from src.ecs.components.tags.c_tag_bullet_enemy import CTagBulletEnemy
from src.ecs.components.tags.c_tag_bullet_player import CTagBulletPlayer
from src.ecs.components.tags.c_tag_high_score import CTagHighScore
from src.ecs.components.tags.c_tag_player_lives import CTagPlayerLives
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
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_score import CTagScore


def create_background(ecs_world: esper.World):
    background_data = ServiceLocator.configs_service.get("assets/cfg/starfield.json")
    number_of_stars = background_data["number_of_stars"]
    speed_range = (
        background_data["vertical_speed"]["min"],
        background_data["vertical_speed"]["max"],
    )
    blink_rate_range = (
        background_data["blink_rate"]["min"],
        background_data["blink_rate"]["max"],
    )
    star_colors = background_data["star_colors"]
    for _ in range(number_of_stars):
        star_entity = ecs_world.create_entity()

        size = pygame.Vector2(1, 1)
        color_choice = random.choice(star_colors)
        color = pygame.color.Color(
            color_choice["r"], color_choice["g"], color_choice["b"]
        )

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


def create_sprite(
    ecs_world: esper.World,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    surface: pygame.Surface,
) -> int:
    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, CTransform(pos))
    ecs_world.add_component(sprite_entity, CVelocity(vel))
    ecs_world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity


def create_square(
    ecs_world: esper.World,
    size: pygame.Vector2,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    col: pygame.Color,
) -> int:
    square_entity = ecs_world.create_entity()
    ecs_world.add_component(square_entity, CSurface(size, col))
    ecs_world.add_component(square_entity, CTransform(pos))
    ecs_world.add_component(square_entity, CVelocity(vel))
    return square_entity


def create_title_logo(ecs_world: esper.World):
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    logo_data = interface_data["game_logo"]
    logo_surface = ServiceLocator.images_service.get(logo_data["image"])

    vel = pygame.Vector2(0, 0)
    pos = pygame.Vector2(
        logo_data["pos"]["x"] - (logo_surface.get_width() / 2), logo_data["pos"]["y"]
    )

    logo_entity = create_sprite(ecs_world, pos, vel, logo_surface)
    ecs_world.add_component(logo_entity, CVelocity(pygame.Vector2(0, 0)))
    ecs_world.add_component(
        logo_entity,
        CVerticalCard(logo_data["logo_speed"], pos.y + logo_data["logo_offset"], pos.y),
    )


def create_player(ecs_world: esper.World):
    player_data = ServiceLocator.configs_service.get("assets/cfg/player.json")
    surface = ServiceLocator.images_service.get(player_data["image"])
    pos = pygame.Vector2(
        player_data["start_point"]["x"], player_data["start_point"]["y"]
    )
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(ecs_world, pos, vel, surface)
    ecs_world.add_component(player_entity, CTagPlayer(player_data["input_speed"]))
    ecs_world.add_component(player_entity, CPlayerStatus(player_data["lives"]))
    player_tr = ecs_world.component_for_entity(player_entity, CTransform)
    player_v = ecs_world.component_for_entity(player_entity, CVelocity)
    player_tag = ecs_world.component_for_entity(player_entity, CTagPlayer)
    player_status = ecs_world.component_for_entity(player_entity, CPlayerStatus)
    player_surface = ecs_world.component_for_entity(player_entity, CSurface)
    return (
        player_entity,
        player_tr,
        player_v,
        player_tag,
        player_status,
        player_surface,
    )


def create_input_player(ecs_world: esper.World):
    # keyboard
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    pause_game = ecs_world.create_entity()
    # mouse
    input_fire = ecs_world.create_entity()

    ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    ecs_world.add_component(input_fire, CInputCommand("PLAYER_FIRE", pygame.K_z))
    ecs_world.add_component(pause_game, CInputCommand("PAUSE_GAME", pygame.K_p))


def create_player_bullet(
    ecs_world: esper.World, player_position: pygame.Vector2, player_size: pygame.Vector2
):
    bullet_data = ServiceLocator.configs_service.get("assets/cfg/bullet.json")
    bullet_size = pygame.Vector2(
        bullet_data["player"]["size"]["w"], bullet_data["player"]["size"]["h"]
    )
    position = pygame.Vector2(
        player_position.x + (player_size[0] / 2) - (bullet_size[0] / 2),
        player_position.y + (player_size[1] / 2) - (bullet_size[1] / 2),
    )

    vel = pygame.Vector2(
        bullet_data["player"]["velocity"]["x"], bullet_data["player"]["velocity"]["y"]
    )
    size = pygame.Vector2(
        bullet_data["player"]["size"]["w"], bullet_data["player"]["size"]["h"]
    )
    color = pygame.Color(
        bullet_data["player"]["color"]["r"],
        bullet_data["player"]["color"]["g"],
        bullet_data["player"]["color"]["b"],
    )

    bullet_entity = create_square(ecs_world, size, position, vel, color)

    ecs_world.add_component(bullet_entity, CTagBulletPlayer())
    ServiceLocator.sounds_service.play(bullet_data["player"]["sound"])


def create_enemy_bullet(
    ecs_world: esper.World, enemy_position: pygame.Vector2, enemy_size: pygame.Vector2
):
    bullet_data = ServiceLocator.configs_service.get("assets/cfg/bullet.json")
    bullet_size = pygame.Vector2(
        bullet_data["enemy"]["size"]["w"], bullet_data["enemy"]["size"]["h"]
    )
    position = pygame.Vector2(
        enemy_position.x + (enemy_size[0] / 2) - (bullet_size[0] / 2),
        enemy_position.y + (enemy_size[1] / 2) - (bullet_size[1] / 2),
    )

    vel = pygame.Vector2(
        bullet_data["enemy"]["velocity"]["x"], bullet_data["enemy"]["velocity"]["y"]
    )
    size = pygame.Vector2(
        bullet_data["enemy"]["size"]["w"], bullet_data["enemy"]["size"]["h"]
    )
    color = pygame.Color(
        bullet_data["enemy"]["color"]["r"],
        bullet_data["enemy"]["color"]["g"],
        bullet_data["enemy"]["color"]["b"],
    )

    bullet_entity = create_square(ecs_world, size, position, vel, color)

    ecs_world.add_component(bullet_entity, CTagBulletEnemy())


def create_text(
    world: esper.World,
    text: str,
    font: pygame.font.Font,
    color: pygame.Color,
    pos: pygame.Vector2,
):
    text_entity = world.create_entity()
    world.add_component(text_entity, CTransform(pos))
    world.add_component(text_entity, CSurface.from_text(text, font, color))
    return text_entity


def create_press_start_game_text(ecs_world: esper.World) -> None:
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    title_text_data = interface_data["title_text"]
    title_text_color = pygame.color.Color(
        title_text_data["color"]["r"],
        title_text_data["color"]["g"],
        title_text_data["color"]["b"],
    )
    title_text_pos = pygame.Vector2(
        title_text_data["position"]["x"], title_text_data["position"]["y"]
    )
    title_text_font = ServiceLocator.fonts_service.get(
        interface_data["font"], title_text_data["size"]
    )

    start_text = create_text(
        ecs_world,
        title_text_data["text"],
        title_text_font,
        title_text_color,
        title_text_pos,
    )

    blink_rate = title_text_data["blink_rate"]
    ecs_world.add_component(start_text, CBlink(blink_rate))
    ecs_world.add_component(start_text, CVelocity(pygame.Vector2(0, 0)))
    ecs_world.add_component(
        start_text,
        CVerticalCard(
            interface_data["game_logo"]["logo_speed"],
            title_text_pos.y + interface_data["game_logo"]["logo_offset"],
            title_text_pos.y,
        ),
    )


def create_paused_text(ecs_world: esper.World):
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    pause_text_data = interface_data["pause_text"]
    font = ServiceLocator.fonts_service.get(
        interface_data["font"], pause_text_data["size"]
    )
    color = pygame.Color(
        pause_text_data["color"]["r"],
        pause_text_data["color"]["g"],
        pause_text_data["color"]["b"],
    )
    blink_rate = pause_text_data["blink_rate"]
    position = pygame.Vector2(
        pause_text_data["position"]["x"], pause_text_data["position"]["y"]
    )
    text = pause_text_data["text"]
    pause_text = create_text(ecs_world, text, font, color, position)
    ecs_world.add_component(pause_text, CBlink(blink_rate))
    return pause_text


def create_game_start_text(ecs_world: esper.World) -> int:
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    game_start_text_data = interface_data["game_start_text"]
    font = ServiceLocator.fonts_service.get(
        interface_data["font"], game_start_text_data["size"]
    )
    color = pygame.Color(
        game_start_text_data["color"]["r"],
        game_start_text_data["color"]["g"],
        game_start_text_data["color"]["b"],
    )
    position = pygame.Vector2(
        game_start_text_data["position"]["x"], game_start_text_data["position"]["y"]
    )
    text = game_start_text_data["text"]
    game_start_text = create_text(ecs_world, text, font, color, position)

    return game_start_text


def create_explosion(ecs_world: esper.World, pos: pygame.Vector2, type: str):
    explosion_data = ServiceLocator.configs_service.get("assets/cfg/explosions.json")
    explosion_data = explosion_data[type]
    explosion_surface = ServiceLocator.images_service.get(explosion_data["image"])

    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(ecs_world, pos, vel, explosion_surface)
    c_surface = ecs_world.component_for_entity(explosion_entity, CSurface)
    animation_data = explosion_data["animations"]
    rect_surf = c_surface.surf.get_rect()
    c_surface.area.w = rect_surf.w / animation_data["number_frames"]
    c_surface.area.x = c_surface.area.w * 1
    ecs_world.add_component(explosion_entity, CTagExplosion())
    ecs_world.add_component(explosion_entity, CAnimation(explosion_data["animations"]))
    ServiceLocator.sounds_service.play(explosion_data["sound"])
    return explosion_entity


def create_enemy(
    ecs_world: esper.World,
    pos: pygame.Vector2,
    velocity: pygame.Vector2,
    score_value: float,
    image_path: str,
    animations: dict,
) -> None:
    image = ServiceLocator.images_service.get(image_path)
    enemy_entity = create_sprite(ecs_world, pos, velocity, image)
    ecs_world.add_component(enemy_entity, CTagEnemy(score_value))
    ecs_world.add_component(enemy_entity, CAnimation(animations))


def create_all_enemies(ecs_world: esper.World):
    enemies_level = ServiceLocator.configs_service.get("assets/cfg/level_01.json")
    enemies_info = enemies_level["enemies_info"]
    enemies_data = ServiceLocator.configs_service.get("assets/cfg/enemies.json")

    for enemy_info in enemies_info:
        enemy_config = None
        if enemy_info["enemy_type"] == "Type1":
            enemy_config = enemies_data["enemy_01"]
        elif enemy_info["enemy_type"] == "Type2":
            enemy_config = enemies_data["enemy_02"]
        elif enemy_info["enemy_type"] == "Type3":
            enemy_config = enemies_data["enemy_03"]
        elif enemy_info["enemy_type"] == "Type4":
            enemy_config = enemies_data["enemy_04"]

        score_value = enemy_config["score_value"]
        image = enemy_config["image"]
        animations = enemy_config["animations"]
        vel = pygame.Vector2(1, 0) * enemies_level["velocity"]
        create_enemy(
            ecs_world,
            pygame.Vector2(enemy_info["position"]["x"], enemy_info["position"]["y"]),
            vel,
            score_value,
            image,
            animations,
        )


def create_menu_text(ecs_world: esper.World):
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")

    # 1UP Label
    one_up_label_data = interface_data["1_up_label"]
    one_up_label_color = pygame.color.Color(
        one_up_label_data["color"]["r"],
        one_up_label_data["color"]["g"],
        one_up_label_data["color"]["b"],
    )
    one_up_label_pos = pygame.Vector2(
        one_up_label_data["position"]["x"], one_up_label_data["position"]["y"]
    )
    one_up_label_font = ServiceLocator.fonts_service.get(
        interface_data["font"], one_up_label_data["size"]
    )

    one_up_label = create_text(
        ecs_world,
        one_up_label_data["text"],
        one_up_label_font,
        one_up_label_color,
        one_up_label_pos,
    )

    ecs_world.add_component(one_up_label, CVelocity(pygame.Vector2(0, 0)))
    ecs_world.add_component(
        one_up_label,
        CVerticalCard(
            one_up_label_data["speed"],
            one_up_label_pos.y + one_up_label_data["offset"],
            one_up_label_pos.y,
        ),
    )

    # 1UP Text
    one_up_text_data = interface_data["1_up_text"]
    one_up_text_color = pygame.color.Color(
        one_up_text_data["color"]["r"],
        one_up_text_data["color"]["g"],
        one_up_text_data["color"]["b"],
    )
    one_up_text_pos = pygame.Vector2(
        one_up_text_data["position"]["x"], one_up_text_data["position"]["y"]
    )
    one_up_text_font = ServiceLocator.fonts_service.get(
        interface_data["font"], one_up_text_data["size"]
    )

    one_up_text = create_text(
        ecs_world,
        one_up_text_data["text"],
        one_up_text_font,
        one_up_text_color,
        one_up_text_pos,
    )
    ecs_world.add_component(one_up_text, CTagScore())
    ecs_world.add_component(one_up_text, CVelocity(pygame.Vector2(0, 0)))
    ecs_world.add_component(
        one_up_text,
        CVerticalCard(
            one_up_text_data["speed"],
            one_up_text_pos.y + one_up_text_data["offset"],
            one_up_text_pos.y,
        ),
    )

    # Hi-Score Label
    hi_score_label_data = interface_data["hi_score_label"]
    hi_score_label_color = pygame.color.Color(
        hi_score_label_data["color"]["r"],
        hi_score_label_data["color"]["g"],
        hi_score_label_data["color"]["b"],
    )
    hi_score_label_pos = pygame.Vector2(
        hi_score_label_data["position"]["x"], hi_score_label_data["position"]["y"]
    )
    hi_score_label_font = ServiceLocator.fonts_service.get(
        interface_data["font"], hi_score_label_data["size"]
    )

    hi_score_label = create_text(
        ecs_world,
        hi_score_label_data["text"],
        hi_score_label_font,
        hi_score_label_color,
        hi_score_label_pos,
    )

    ecs_world.add_component(hi_score_label, CVelocity(pygame.Vector2(0, 0)))
    ecs_world.add_component(
        hi_score_label,
        CVerticalCard(
            hi_score_label_data["speed"],
            hi_score_label_pos.y + hi_score_label_data["offset"],
            hi_score_label_pos.y,
        ),
    )

    # Hi-Score Text
    hi_score_text_data = interface_data["hi_score_text"]
    hi_score_text_color = pygame.color.Color(
        hi_score_text_data["color"]["r"],
        hi_score_text_data["color"]["g"],
        hi_score_text_data["color"]["b"],
    )
    hi_score_text_pos = pygame.Vector2(
        hi_score_text_data["position"]["x"], hi_score_text_data["position"]["y"]
    )
    hi_score_text_font = ServiceLocator.fonts_service.get(
        interface_data["font"], hi_score_text_data["size"]
    )
    text = hi_score_text_data['text']
    ServiceLocator.globals_service.player_high_score = int(text) if ServiceLocator.globals_service.player_high_score < int(text) else ServiceLocator.globals_service.player_high_score
    hi_score_text = create_text(
        ecs_world,
        str(ServiceLocator.globals_service.player_high_score),
        hi_score_text_font,
        hi_score_text_color,
        hi_score_text_pos,
    )

    ecs_world.add_component(hi_score_text, CVelocity(pygame.Vector2(0, 0)))
    ecs_world.add_component(
        hi_score_text,
        CVerticalCard(
            hi_score_text_data["speed"],
            hi_score_text_pos.y + hi_score_text_data["offset"],
            hi_score_text_pos.y,
        ),
    )
    ecs_world.add_component(hi_score_text, CTagHighScore())


def show_game_over(ecs_world: esper.World):
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    game_over_text_data = interface_data["game_over_text"]
    game_over_text_color = pygame.color.Color(
        game_over_text_data["color"]["r"],
        game_over_text_data["color"]["g"],
        game_over_text_data["color"]["b"],
    )
    game_over_text_pos = pygame.Vector2(
        game_over_text_data["position"]["x"], game_over_text_data["position"]["y"]
    )
    game_over_text_font = ServiceLocator.fonts_service.get(
        interface_data["font"], game_over_text_data["size"]
    )

    game_over_text = create_text(
        ecs_world,
        game_over_text_data["text"],
        game_over_text_font,
        game_over_text_color,
        game_over_text_pos,
    )
    ecs_world.add_component(game_over_text, CVelocity(pygame.Vector2(0, 0)))


def show_next_level(ecs_world: esper.World):
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    next_level_text_data = interface_data["next_level_text"]
    next_level_text_color = pygame.color.Color(
        next_level_text_data["color"]["r"],
        next_level_text_data["color"]["g"],
        next_level_text_data["color"]["b"],
    )
    next_level_text_pos = pygame.Vector2(
        next_level_text_data["position"]["x"], next_level_text_data["position"]["y"]
    )
    next_level_text_font = ServiceLocator.fonts_service.get(
        interface_data["font"], next_level_text_data["size"]
    )

    next_level_text = create_text(
        ecs_world,
        next_level_text_data["text"],
        next_level_text_font,
        next_level_text_color,
        next_level_text_pos,
    )
    ecs_world.add_component(next_level_text, CVelocity(pygame.Vector2(0, 0)))

    get_ready_text_data = interface_data["get_ready_text"]
    get_ready_text_color = pygame.color.Color(
        get_ready_text_data["color"]["r"],
        get_ready_text_data["color"]["g"],
        get_ready_text_data["color"]["b"],
    )
    get_ready_text_pos = pygame.Vector2(
        get_ready_text_data["position"]["x"], get_ready_text_data["position"]["y"]
    )
    get_ready_text_font = ServiceLocator.fonts_service.get(
        interface_data["font"], get_ready_text_data["size"]
    )

    get_ready_text = create_text(
        ecs_world,
        get_ready_text_data["text"],
        get_ready_text_font,
        get_ready_text_color,
        get_ready_text_pos,
    )
    ecs_world.add_component(get_ready_text, CVelocity(pygame.Vector2(0, 0)))


def create_lives(ecs_world: esper.World):
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    lives_data = interface_data["lives"]
    lives_surface = ServiceLocator.images_service.get(lives_data["image"])
    lives_pos = pygame.Vector2(lives_data["position"]["x"], lives_data["position"]["y"])
    lives_vel = pygame.Vector2(0, 0)

    for i in range(ServiceLocator.globals_service.player_lives):
        pos = pygame.Vector2(lives_pos.x + (i * 10), lives_pos.y)
        lives_entity = create_sprite(ecs_world, pos, lives_vel, lives_surface)
        ecs_world.add_component(lives_entity, CVelocity(lives_vel))
        ecs_world.add_component(lives_entity, CTagPlayerLives())


def show_level(ecs_world: esper.World):
    interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
    level_text_data = interface_data["level_text"]
    level_text_color = pygame.color.Color(
        level_text_data["color"]["r"],
        level_text_data["color"]["g"],
        level_text_data["color"]["b"],
    )
    level_text_pos = pygame.Vector2(
        level_text_data["position"]["x"], level_text_data["position"]["y"]
    )
    level_text_font = ServiceLocator.fonts_service.get(
        interface_data["font"], level_text_data["size"]
    )

    level_text = create_text(
        ecs_world,
        convert_double_digit(ServiceLocator.globals_service.current_level),
        level_text_font,
        level_text_color,
        level_text_pos,
    )
    ecs_world.add_component(level_text, CVelocity(pygame.Vector2(0, 0)))
    # Load and show image
    level_image_data = interface_data["level_flag"]
    level_image = ServiceLocator.images_service.get(level_image_data["image"])
    level_image_pos = pygame.Vector2(
        level_image_data["position"]["x"], level_image_data["position"]["y"]
    )
    create_sprite(ecs_world, level_image_pos, pygame.Vector2(0, 0), level_image)
