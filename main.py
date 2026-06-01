from src.core.settings import load_config
from src.utils.logger import get_logger


logger = get_logger(__name__)

config = load_config()

logger.info("Application started")

print(config)