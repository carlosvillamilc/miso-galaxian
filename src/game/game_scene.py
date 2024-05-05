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
        (self.player_entity, 
         self.player_transform, 
         self.player_vel, 
         self.player_tag, 
         self.player_status,
         self.player_surface) = create_player(self.ecs_world, self._game_engine.player_cfg)
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
                self.player_vel.vel.x -= self.player_tag.input_speed
            else:
                self.player_vel.vel.x += self.player_tag.input_speed
        if action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                self.player_vel.vel.x += self.player_tag.input_speed
            else:
                self.player_vel.vel.x -= self.player_tag.input_speed
        if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START:
            #breakpoint()
            create_bullet(self.ecs_world,self.player_transform.pos, self.player_surface.area.size, self._game_engine.bullet_cfg)

    def do_process_events(self, event: pygame.Event) -> None:
        #breakpoint()
        super().do_process_events(event)
        # Check if key space is pressed and switch to manu scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_scene("MENU_SCENE")
