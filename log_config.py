import logging
from config import system_config

logger = logging.getLogger()
logger.setLevel(system_config.log_level)