import pygame

# Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.tags.c_tag_bullet_player import CTagBulletPlayer
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_fire_enemy import system_fire_enemy
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

from src.create.prefab_creator import (
    create_background,
    create_player,
    create_input_player,
    create_player_bullet,
    create_paused_text,
    create_game_start_text,
    create_all_enemies,
    create_menu_text,
)


class GameScene(Scene):

    def do_create(self):
        print("GameScene created")
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
        # create_game_start_text(self.ecs_world,self._game_engine.interface_cfg)
        create_all_enemies(self.ecs_world)
        create_menu_text(self.ecs_world)

    def do_update(self, delta_time):
        system_blink(self.ecs_world, delta_time)
        if ServiceLocator.globals_service.paused:
            return
        # if self._game_engine.game_paused:
        #    return
        # print("GameScene updated")
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
        system_update_score(
            self.ecs_world,
            ServiceLocator.globals_service.player_score,
            ServiceLocator.globals_service.player_previous_score,
        )

    def do_action(self, action: CInputCommand):
        print("GameScene action", action.name)
        # breakpoint()
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
            # breakpoint()
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
        # breakpoint()
        super().do_process_events(event)
        # Check if key space is pressed and switch to manu scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_scene("MENU_SCENE")
