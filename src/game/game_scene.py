import pygame

# Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator

from src.ecs.systems.s_background import system_background
from src.ecs.systems.s_player_movement import system_player_movement
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_blink import system_blink

from src.create.prefab_creator import (create_background, 
                                       create_player,
                                       create_input_player,
                                       create_bullet,
                                       create_paused_text,
                                       create_game_start_text)

class GameScene(Scene):

    def do_create(self):
        print("GameScene created")
        create_background(self.ecs_world)
        (self.player_entity, 
         self.player_transform, 
         self.player_vel, 
         self.player_tag, 
         self.player_status,
         self.player_surface) = create_player(self.ecs_world)
        create_input_player(self.ecs_world)
        #create_game_start_text(self.ecs_world)

    def do_update(self, delta_time):
        system_blink(self.ecs_world, delta_time)
        if ServiceLocator.globals_service.paused:
            return
        #if self._game_engine.game_paused: 
        #    return
        #print("GameScene updated")
        system_movement(self.ecs_world, delta_time)
        system_background(self.ecs_world, self._game_engine.screen, delta_time)
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
            if ServiceLocator.globals_service.paused:
                return
            #breakpoint()
            create_bullet(self.ecs_world,self.player_transform.pos, self.player_surface.area.size)
        if action.name == "PAUSE_GAME" and action.phase == CommandPhase.START:
            ServiceLocator.globals_service.paused = not ServiceLocator.globals_service.paused
            if ServiceLocator.globals_service.paused:
                self.paused_text = create_paused_text(self.ecs_world)
                sounds_data = ServiceLocator.configs_service.get("assets/cfg/sounds.json")
                ServiceLocator.sounds_service.play(sounds_data["pause_game"])

            else:
                self.ecs_world.delete_entity(self.paused_text)
            
            

    def do_process_events(self, event: pygame.Event) -> None:
        #breakpoint()
        super().do_process_events(event)
        # Check if key space is pressed and switch to manu scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_scene("MENU_SCENE")
