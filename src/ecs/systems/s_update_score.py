import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_score import CTagScore
from src.engine.service_locator import ServiceLocator


def system_update_score(world: esper.World, new_score: int, previous_score: int):
    if new_score != previous_score:
        ServiceLocator.globals_service.player_previous_score = new_score
        interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
        one_up_text_data = interface_data["1_up_text"]
        one_up_text_font = ServiceLocator.fonts_service.get(
            interface_data["font"], one_up_text_data["size"]
        )
        one_up_text_color = pygame.color.Color(*one_up_text_data["color"].values())
        components = world.get_components(CSurface, CTagScore)
        c_surface: CSurface
        for entity, (c_surface, _) in components:
            c_surface.set_text(str(new_score), one_up_text_font, one_up_text_color)
