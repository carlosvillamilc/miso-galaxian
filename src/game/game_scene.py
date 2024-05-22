from enum import Enum
import pygame
import json

# Scene
from src.create.prefab_creator_debug import create_debug_input, create_editor_placer
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.editor.c_editor_draggable import CEditorDraggable
from src.ecs.components.editor.c_editor_place import CEditorPlacer
from src.ecs.components.tags.c_tag_bullet_player import CTagBulletPlayer
from src.ecs.components.c_game_manager import CGameManager
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_ghost import CTagEnemyGhost
from src.ecs.systems.debug.s_rendering_debug_rects import system_rendering_debug_rects
from src.ecs.systems.debug.s_rendering_debug_velocity import system_rendering_debug_velocity
from src.ecs.systems.editor.s_editor_draggable import system_editor_draggable
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_enemy_steering import system_enemy_steering
from src.ecs.systems.s_fire_enemy import system_fire_enemy
from src.ecs.systems.s_follow_mouse import system_follow_mouse
from src.ecs.systems.s_rendering import system_rendering
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
    create_all_enemies,
    create_background,
    create_editor_text,
    create_editor_text_saved,
    create_enemy,
    create_lives,
    create_player,
    create_input_player,
    create_player_bullet,
    create_paused_text,
    create_game_start_text,
    create_menu_text,
    show_level,
)
import src.engine.game_engine

class DebugView(Enum):
    NONE = 0,
    RECTS = 1,
    VELOCITY = 2

class GameScene(Scene):

    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self.player_explosion_time = 0
        self._debug_view = DebugView.NONE
        self._editor_mode = False
        self._sounds_data = ServiceLocator.configs_service.get("assets/cfg/sounds.json")
        self.enemies_cfg = ServiceLocator.configs_service.get("assets/cfg/enemies.json")
        self.editor_cursor_cfg = ServiceLocator.configs_service.get("assets/cfg/editor_cursor.json")
        self.level_cfg = ServiceLocator.configs_service.get("assets/cfg/level_1.json")
        self.window_cfg = ServiceLocator.configs_service.get("assets/cfg/window.json")
        self._mouse_pos = pygame.Vector2(0, 0)

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
        create_debug_input(self.ecs_world)
        start_game_entity = create_game_start_text(self.ecs_world)
        self.game_manager = CGameManager(start_game_entity)
        create_lives(self.ecs_world)
        show_level(self.ecs_world)
        create_menu_text(self.ecs_world)

        placer_entity = create_editor_placer(self.ecs_world)
        self.placer_s = self.ecs_world.component_for_entity(placer_entity, CSurface)
        self.placer_t = self.ecs_world.component_for_entity(placer_entity, CTransform)
        self.placer_ed = self.ecs_world.component_for_entity(placer_entity, CEditorPlacer)

        editor_text_entity = create_editor_text(self.ecs_world)
        self.editor_text_s = self.ecs_world.component_for_entity(editor_text_entity, CSurface)

        editor_text_saved_entity = create_editor_text_saved(self.ecs_world)
        self.editor_text_saved_s = self.ecs_world.component_for_entity(editor_text_saved_entity, CSurface)

        self.placer_s.visible = False
        self.editor_text_s.visible = False
        self.editor_text_saved_s.visible = False
        self.game_over = False

    def do_update(self, delta_time, elapsed_time):
        system_blink(self.ecs_world, delta_time)
        system_background(self.ecs_world, self._game_engine.screen, delta_time)

        if self._editor_mode:
            system_follow_mouse(self.ecs_world, self._mouse_pos)
            system_editor_draggable(self.ecs_world, self._mouse_pos)

        if ServiceLocator.globals_service.paused:
            return
        system_movement(self.ecs_world, delta_time)
        system_enemy_movement(self.ecs_world)
        
        if not self.game_over:
            system_enemy_steering(self.ecs_world, self.player_entity, 1, delta_time)
            system_fire_enemy(self.ecs_world)
            self.player_explosion_time = system_collision_player_enemy(self.ecs_world, self.player_entity, elapsed_time, self.player_explosion_time)
            self.player_explosion_time = system_collision_bullet_player(self.ecs_world, self.player_entity, elapsed_time, self.player_explosion_time)
            system_player_movement(self.ecs_world, self._game_engine.screen)

        system_screen_bullet(self.ecs_world, self._game_engine.screen)
        self.bullets = len(self.ecs_world.get_component(CTagBulletPlayer))
        system_animation(self.ecs_world, delta_time)
        system_collision_bullet_enemy(self.ecs_world)
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
        system_game_over(self.ecs_world, self.game_over, self.set_game_over, self.player_entity)
        system_game_manager(self.ecs_world, self.game_manager, delta_time, ServiceLocator.globals_service.current_level)

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
            elif action.phase == CommandPhase.END and action.input_start == True:
                self.player_vel.vel.x += self.player_tag.input_speed
        elif action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                self.player_vel.vel.x += self.player_tag.input_speed
            elif action.phase == CommandPhase.END and action.input_start == True:
                self.player_vel.vel.x -= self.player_tag.input_speed

        if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START:
            if ServiceLocator.globals_service.paused:
                return

            player_has_surface = self.ecs_world.has_component(
                self.player_entity, CSurface
            )
            if self.bullets < 1 and player_has_surface:
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
                ServiceLocator.sounds_service.play(self._sounds_data["pause_game"])

            else:
                self.ecs_world.delete_entity(self.paused_text)

        if action.name == "TOGGLE_DEBUG_VIEW" and action.phase == CommandPhase.START:
            if self._debug_view == DebugView.NONE:
                self._debug_view = DebugView.RECTS
            elif self._debug_view == DebugView.RECTS:
                self._debug_view = DebugView.VELOCITY
            elif self._debug_view == DebugView.VELOCITY:
                self._debug_view = DebugView.NONE
        
        if action.name == "TOGGLE_EDITOR" and action.phase == CommandPhase.START:
            enemy_components = self.ecs_world.get_components(CTagEnemy)
            if len(enemy_components) > 0:
                self._editor_mode = not self._editor_mode
                self.placer_s.visible = self._editor_mode
                self.editor_text_s.visible = self._editor_mode
                self._player_cfg = ServiceLocator.configs_service.get("assets/cfg/player.json")
                if self._editor_mode:
                    self.player_transform.x = self._player_cfg["start_point"]["x"]
                    self.player_transform.y = self._player_cfg["start_point"]["y"]
                    ServiceLocator.globals_service.paused = True
                    self.paused_text = create_paused_text(self.ecs_world)
                    ServiceLocator.sounds_service.play(self._sounds_data["pause_game"])
                
        if self._editor_mode:
            self._do_editor_action(action)
                
    def do_draw(self, screen):
        if not self._debug_view == DebugView.RECTS:
            system_rendering(self.ecs_world, screen)
        else:
            system_rendering_debug_rects(self.ecs_world, screen)

        if self._debug_view == DebugView.VELOCITY:
            system_rendering_debug_velocity(self.ecs_world, screen)

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
        create_debug_input(self.ecs_world)
        create_all_enemies(self.ecs_world, ServiceLocator.globals_service.current_level)
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

    def _do_editor_action(self, action:CInputCommand):
        if action.name == "MOUSE_MOVE":
            self._mouse_pos = action.mouse_pos
        
        if action.name == "DRAG_BLOCK":
            enemy_type = self.placer_ed.types[self.placer_ed.curr_type_idx]
            if enemy_type is None:
                if action.phase == CommandPhase.START:
                    components = self.ecs_world.get_components(CTransform, CSurface, CEditorDraggable)

                    c_t:CTransform
                    c_s:CSurface
                    c_ed:CEditorDraggable
                    for _, (c_t, c_s, c_ed) in components:
                        surf_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
                        placer_rect = CSurface.get_area_relative(self.placer_s.area, self.placer_t.pos)
                        if surf_rect.colliderect(placer_rect):
                            c_ed.is_dragging = True
                else:
                    components = self.ecs_world.get_component(CEditorDraggable)

                    c_ed:CEditorDraggable
                    for _, c_ed in components:
                        c_ed.is_dragging = False                
                self.editor_text_saved_s.visible = False
            
        if action.name == "CHANGE_ENTITY" and action.phase == CommandPhase.START:
            self.placer_ed.curr_type_idx += 1
            self.placer_ed.curr_type_idx %= len(self.placer_ed.types)
            enemy_type = self.placer_ed.types[self.placer_ed.curr_type_idx]
            if enemy_type is not None:
                self.placer_s.surf = ServiceLocator.images_service.get(self.enemies_cfg[enemy_type]["placer_image"])
                self.placer_s.area = self.placer_s.surf.get_rect()
            else:
                self.placer_s.surf = pygame.Surface((self.editor_cursor_cfg["size"]["x"], self.editor_cursor_cfg["size"]["y"]))
                self.placer_s.surf.fill(pygame.Color(self.editor_cursor_cfg["color"]["r"], self.editor_cursor_cfg["color"]["g"], self.editor_cursor_cfg["color"]["b"]))
                self.placer_s.area = self.placer_s.surf.get_rect()
            self.editor_text_saved_s.visible = False

        if action.name == "PLACE_ENTITY" and action.phase == CommandPhase.START:
            enemy_type = self.placer_ed.types[self.placer_ed.curr_type_idx]
            if enemy_type is not None:
                enemy_config = self.enemies_cfg[enemy_type]
                pos = self._mouse_pos - pygame.Vector2(1, 1)
                vel = pygame.Vector2(1, 0) * self.level_cfg["velocity"]
                score_value = enemy_config["score_value"]
                image = enemy_config["image"]
                animations = enemy_config["animations"]
                index = self._get_max_index_enemies()

                components = self.ecs_world.get_components(CVelocity, CTagEnemy)

                c_v:CVelocity
                for _, (c_v, _) in components:
                    vel = c_v.vel
                    break

                if pos.x > 20 and pos.x <= self.window_cfg["size"]["w"] - 35:
                    create_enemy(self.ecs_world, pos, vel, score_value, image, animations, index + 1, enemy_type)

                self.editor_text_saved_s.visible = False
        
        if action.name == "DELETE_ENTITY" and action.phase == CommandPhase.START:
            enemy_type = self.placer_ed.types[self.placer_ed.curr_type_idx]
            if enemy_type is None:
                components = self.ecs_world.get_components(CTransform, CSurface, CEditorDraggable, CTagEnemy)

                c_t:CTransform
                c_s:CSurface
                c_te:CTagEnemy
                for enemy_entity, (c_t, c_s, _, c_te) in components:
                    surf_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
                    placer_rect = CSurface.get_area_relative(self.placer_s.area, self.placer_t.pos)
                    if surf_rect.colliderect(placer_rect):
                        enemy_ghost_components = self.ecs_world.get_component(CTagEnemyGhost)

                        c_teg:CTagEnemyGhost
                        for enemy_ghost_entity, c_teg in enemy_ghost_components:
                            if c_teg.index == c_te.index:
                                self.ecs_world.delete_entity(enemy_ghost_entity)
                                break

                        self.ecs_world.delete_entity(enemy_entity)
                self.editor_text_saved_s.visible = False

        if action.name == "SAVE_LEVEL" and action.phase == CommandPhase.START:
            level = {}
            level["follow_force"] = 125
            level["velocity"] = 10
            level["enemies_info"] = []
            components = self.ecs_world.get_components(CTransform, CTagEnemy)

            c_t:CTransform
            c_te:CTagEnemy
            for _, (c_t, c_te) in components:
                enemy_info = {}
                enemy_info["enemy_type"] = c_te.type
                enemy_info["position"] = {}
                enemy_info["position"]["x"] = c_t.pos.x
                enemy_info["position"]["y"] = c_t.pos.y
                level["enemies_info"].append(enemy_info)
            
            with open("assets/cfg/editor_level.json", "w") as write_file:
                json.dump(level, write_file, indent=4)

            self.editor_text_saved_s.visible = True

    def _get_max_index_enemies(self) -> int:
        max_index:int = 0
        components = self.ecs_world.get_component(CTagEnemy)

        c_te:CTagEnemy
        for _, c_te in components:
            if c_te.index > max_index:
                max_index = c_te.index

        return max_index

    def _do_clean(self):
        self._debug_view = DebugView.NONE
        ServiceLocator.globals_service.paused = False
        self._editor_mode = False