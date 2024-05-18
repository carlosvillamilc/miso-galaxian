import esper
from src.ecs.components.tags.c_tag_player_lives import CTagPlayerLives
from src.engine.service_locator import ServiceLocator


def system_update_lives(ecs_world: esper.World):
    components = ecs_world.get_components(CTagPlayerLives)
    if components and len(components) > ServiceLocator.globals_service.player_lives:
        last_entity = components[-1][0]
        ecs_world.delete_entity(last_entity)
