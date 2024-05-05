import pygame

# Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.engine.scenes.scene import Scene
from src.ecs.systems.s_background import system_background
from src.ecs.systems.s_player_movement import system_player_movement
from src.ecs.systems.s_movement import system_movement
from src.create.prefab_creator import (create_background, 
                                       create_player,
                                       create_input_player,
                                       create_bullet)
class GameScene(Scene):
    def do_create(self):
        print("GameScene created")
        create_background(self.ecs_world, self._game_engine.starfield_cfg)
        self.pl_entity, self.pl_tr, self.pl_v, self.pl_tg, self.pl_st = create_player(self.ecs_world, self._game_engine.player_cfg)
        create_input_player(self.ecs_world)

    def do_update(self, delta_time):
        #print("GameScene updated")
        system_movement(self.ecs_world, delta_time)
        system_background(self.ecs_world, self._game_engine.screen, self._game_engine.delta_time)
        system_player_movement(self.ecs_world, self._game_engine.screen)



    def do_action(self, action: CInputCommand):
        print("GameScene action", action.name)
        #breakpoint()
        if action.name == "PLAYER_LEFT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x -= self.pl_tg.input_speed
            else:
                self.pl_v.vel.x += self.pl_tg.input_speed
        if action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x += self.pl_tg.input_speed
            else:
                self.pl_v.vel.x -= self.pl_tg.input_speed
        if action.name == "FIRE_NORMAL" and action.phase == CommandPhase.START:
            create_bullet(self.ecs_world, c_input.mouse_position, self._player_transform.pos, self._player_surface.area.size, self.bullet_data)

    def do_process_events(self, event: pygame.Event) -> None:
        #breakpoint()
        super().do_process_events(event)
        # Check if key space is pressed and switch to manu scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_scene("MENU_SCENE")
