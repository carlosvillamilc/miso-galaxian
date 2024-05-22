import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.editor.c_editor_draggable import CEditorDraggable

def system_editor_draggable(world:esper.World, mouse_pos:pygame.Vector2):
    components = world.get_components(CTransform, CEditorDraggable)

    c_t:CTransform
    c_d:CEditorDraggable
    for _, (c_t, c_d) in components:
        if c_d.is_dragging:
            c_t.pos.x = mouse_pos.x
            c_t.pos.y = mouse_pos.y