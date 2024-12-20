# config/logging_config.py
import logging
from colorama import Fore, Style, init

init(autoreset=True)

LOG_COLORS = {
    'DEBUG': Fore.CYAN,
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': Fore.MAGENTA + Style.BRIGHT,
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, "")
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

def setup_logging():
    log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(ColorFormatter(fmt=log_format, datefmt=date_format))
        root_logger.addHandler(handler)

    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    discord_logger.propagate = False
    if not discord_logger.hasHandlers():
        discord_handler = logging.StreamHandler()
        discord_handler.setFormatter(ColorFormatter(fmt=log_format, datefmt=date_format))
        discord_logger.addHandler(discord_handler)

    return root_logger
