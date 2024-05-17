import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_high_score import CTagHighScore
from src.engine.service_locator import ServiceLocator


def system_update_high_score(world: esper.World, high_score: int, player_score: int):
    print("system_update_high_score")
    print(high_score, player_score)
    if high_score < player_score:
        print("updating high score")
        interface_data = ServiceLocator.configs_service.get("assets/cfg/interface.json")
        high_score_text_data = interface_data["hi_score_text"]
        high_score_text_font = ServiceLocator.fonts_service.get(
            interface_data["font"], high_score_text_data["size"]
        )
        high_score_text_color = pygame.color.Color(
            *high_score_text_data["color"].values()
        )
        ServiceLocator.globals_service.player_high_score = player_score
        components = world.get_components(CSurface, CTagHighScore)
        c_surface: CSurface
        for entity, (c_surface, _) in components:
            c_surface.set_text(
                str(player_score), high_score_text_font, high_score_text_color
            )
