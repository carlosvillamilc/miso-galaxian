from src.engine.services.fonts_service import FontsService
from src.engine.services.images_service import ImageService
from src.engine.services.sounds_service import SoundsService
from src.engine.services.configs_service import ConfigsService
from src.engine.services.globals_service import GlobalsService
class ServiceLocator:
    images_service = ImageService()
    sounds_service = SoundsService()
    fonts_service = FontsService()
    configs_service = ConfigsService()
    globals_service = GlobalsService()
