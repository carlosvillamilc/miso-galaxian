import pygame
import time

# Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.tags.c_tag_bullet_player import CTagBulletPlayer
from src.ecs.components.c_game_manager import CGameManager
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_fire_enemy import system_fire_enemy
from src.ecs.systems.s_update_high_score import system_update_high_score
from src.ecs.systems.s_update_lives import system_update_lives
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator

from src.ecs.systems.s_background import system_background
from src.ecs.systems.s_player_movement import system_player_movement
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_bullet_player import system_collision_bullet_player
from src.ecs.systems.s_explosion import system_explosion
from src.ecs.systems.s_update_score import system_update_score
from src.ecs.systems.s_next_level import system_next_level
from src.ecs.systems.s_game_manager import system_game_manager
from src.ecs.systems.s_game_over import system_game_over
from src.create.prefab_creator import (
    create_background,
    create_lives,
    create_player,
    create_input_player,
    create_player_bullet,
    create_paused_text,
    create_game_start_text,
    create_all_enemies,
    create_menu_text,
    show_level,
)


class GameScene(Scene):

    def do_create(self):
        create_background(self.ecs_world)
        (
            self.player_entity,
            self.player_transform,
            self.player_vel,
            self.player_tag,
            self.player_status,
            self.player_surface,
        ) = create_player(self.ecs_world)
        create_input_player(self.ecs_world)
        # create_game_start_text(self.ecs_world, self._game_engine.interface_cfg)
        # create_all_enemies(self.ecs_world)
        start_game_entity = create_game_start_text(self.ecs_world)
        self.game_manager = CGameManager(start_game_entity)
        create_lives(self.ecs_world)
        show_level(self.ecs_world)
        # create_all_enemies(self.ecs_world)
        create_menu_text(self.ecs_world)
        self.game_over = False

    def do_update(self, delta_time):
        system_blink(self.ecs_world, delta_time)
        if ServiceLocator.globals_service.paused:
            return
        system_movement(self.ecs_world, delta_time)
        system_enemy_movement(self.ecs_world)
        system_fire_enemy(self.ecs_world)
        system_background(self.ecs_world, self._game_engine.screen, delta_time)
        system_player_movement(self.ecs_world, self._game_engine.screen)
        system_screen_bullet(self.ecs_world, self._game_engine.screen)
        self.bullets = len(self.ecs_world.get_component(CTagBulletPlayer))
        system_animation(self.ecs_world, delta_time)
        system_collision_bullet_enemy(self.ecs_world)
        system_collision_bullet_player(self.ecs_world)
        system_explosion(self.ecs_world)
        system_update_lives(self.ecs_world)
        system_update_score(
            self.ecs_world,
            ServiceLocator.globals_service.player_score,
            ServiceLocator.globals_service.player_previous_score,
        )
        system_update_high_score(
            self.ecs_world,
            ServiceLocator.globals_service.player_high_score,
            ServiceLocator.globals_service.player_score,
        )
        system_next_level(
            self.ecs_world,
            self.run_next_level,
            self._game_engine.delta_time,
            self.game_manager,
        )
        system_game_over(self.ecs_world, self.game_over, self.set_game_over)
        system_game_manager(self.ecs_world, self.game_manager, delta_time)

    def set_game_over(self, game_over: bool):
        self.game_over = game_over

    def do_action(self, action: CInputCommand):
        if self.game_over:
            if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START:
                self.do_game_over()
            return
        if action.name == "PLAYER_LEFT":
            if action.phase == CommandPhase.START:
                self.player_vel.vel.x -= self.player_tag.input_speed
            else:
                self.player_vel.vel.x += self.player_tag.input_speed
        if action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                self.player_vel.vel.x += self.player_tag.input_speed
            else:
                self.player_vel.vel.x -= self.player_tag.input_speed
        if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START:
            if ServiceLocator.globals_service.paused:
                return
            if self.bullets < 1:
                create_player_bullet(
                    self.ecs_world,
                    self.player_transform.pos,
                    self.player_surface.area.size,
                )
        if action.name == "PAUSE_GAME" and action.phase == CommandPhase.START:
            ServiceLocator.globals_service.paused = (
                not ServiceLocator.globals_service.paused
            )
            if ServiceLocator.globals_service.paused:
                self.paused_text = create_paused_text(self.ecs_world)
                sounds_data = ServiceLocator.configs_service.get(
                    "assets/cfg/sounds.json"
                )
                ServiceLocator.sounds_service.play(sounds_data["pause_game"])

            else:
                self.ecs_world.delete_entity(self.paused_text)

    def do_process_events(self, event: pygame.Event) -> None:
        super().do_process_events(event)

    def do_start_next_level(self):
        self.do_destroy()
        create_background(self.ecs_world)
        (
            self.player_entity,
            self.player_transform,
            self.player_vel,
            self.player_tag,
            self.player_status,
            self.player_surface,
        ) = create_player(self.ecs_world)
        show_level(self.ecs_world)
        create_input_player(self.ecs_world)
        create_all_enemies(self.ecs_world)
        create_menu_text(self.ecs_world)
        create_lives(self.ecs_world)

    def run_next_level(self, delta_time: float):
        cooldown = ServiceLocator.globals_service.next_level_cooldown
        ServiceLocator.globals_service.next_level_cooldown -= delta_time
        if cooldown <= 0:
            ServiceLocator.globals_service.next_level()
            self.do_start_next_level()

    def do_destroy(self):
        self.ecs_world.clear_database()

    def do_game_over(self):
        ServiceLocator.globals_service.game_over()
        self.switch_scene("MENU_SCENE")
