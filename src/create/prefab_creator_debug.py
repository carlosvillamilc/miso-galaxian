import pygame
import esper
from src.create.prefab_creator import create_square
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.editor.c_editor_follow_mouse import CEditorFollowMouse
from src.ecs.components.editor.c_editor_place import CEditorPlacer
from src.engine.service_locator import ServiceLocator

def create_debug_input(world:esper.World):
    swithc_debug_view = world.create_entity()
    world.add_component(swithc_debug_view, CInputCommand("TOGGLE_DEBUG_VIEW", pygame.K_LCTRL))

    switch_editor_mode = world.create_entity()
    world.add_component(switch_editor_mode, CInputCommand("TOGGLE_EDITOR", pygame.K_TAB))

    mouse_move = world.create_entity()
    world.add_component(mouse_move, CInputCommand("MOUSE_MOVE", pygame.MOUSEMOTION))

    mouse_down_left = world.create_entity()
    world.add_component(mouse_down_left, CInputCommand("DRAG_BLOCK", pygame.BUTTON_LEFT))

    place_entity = world.create_entity()
    world.add_component(place_entity, CInputCommand("PLACE_ENTITY", pygame.BUTTON_LEFT))

    mouse_change_entity = world.create_entity()
    world.add_component(mouse_change_entity, CInputCommand("CHANGE_ENTITY", pygame.BUTTON_RIGHT))

    mouse_delete_entity = world.create_entity()
    world.add_component(mouse_delete_entity, CInputCommand("DELETE_ENTITY", pygame.BUTTON_MIDDLE))

    save_level_entity = world.create_entity()
    world.add_component(save_level_entity, CInputCommand("SAVE_LEVEL", pygame.K_RETURN))

def create_editor_placer(world:esper.World):
    placer_cfg = ServiceLocator.configs_service.get("assets/cfg/editor_cursor.json")
    placer_entity = create_square(world, pygame.Vector2(placer_cfg["size"]["x"], placer_cfg["size"]["y"]), pygame.Vector2(0, 0), pygame.Vector2(0, 0),  pygame.Color(placer_cfg["color"]["r"], placer_cfg["color"]["g"], placer_cfg["color"]["b"]))
    placer_s = world.component_for_entity(placer_entity, CSurface)
    placer_s.visible = False
    world.add_component(placer_entity, CEditorFollowMouse())
    world.add_component(placer_entity, CEditorPlacer([None, "enemy_01", "enemy_02", "enemy_03", "enemy_04"]))
    return placer_entity