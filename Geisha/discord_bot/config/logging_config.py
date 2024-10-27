# config/logging_config.py
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    return logging.getLogger(__name__)
