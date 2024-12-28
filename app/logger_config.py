import logging

from .config import system_config, DATETIME_FORMAT, LOGGING_FORMAT

logging.basicConfig(
    level=system_config.log_level,
    format=LOGGING_FORMAT,
    datefmt=DATETIME_FORMAT,
)

logger = logging.getLogger()
