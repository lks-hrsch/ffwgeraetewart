import logging
from logging.handlers import TimedRotatingFileHandler

from src.logic.pathes import log_path

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# add a suffix which you want
file_handler.suffix = "%Y-%m-%d"

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# finally add handler to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
