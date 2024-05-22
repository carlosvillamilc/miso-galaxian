import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.editor.c_editor_follow_mouse import CEditorFollowMouse

def system_follow_mouse(world:esper.World, mouse_pos:pygame.Vector2):
    components = world.get_components(CTransform, CEditorFollowMouse)

    c_t:CTransform
    for _, (c_t, _) in components:
        c_t.pos.x = mouse_pos.x
        c_t.pos.y = mouse_pos.y