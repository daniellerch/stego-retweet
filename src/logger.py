"""
stego-retweet.
"""
import logging
import os

from logging.handlers import RotatingFileHandler
from src import config


def get_file_handler() -> RotatingFileHandler:
    """
    Function to get logger file handler.
    """
    file_handler = RotatingFileHandler(
        f'{config.LOG_PATH}/stego-retweet.log',
        mode='a',
        maxBytes=config.LOG_MAX_MEGABYTES * 1024 * 1024,  # Megabytes
        backupCount=config.LOG_MAX_FILES,
        encoding=None,
        delay=0
    )
    file_handler.setLevel(config.TRACE_LEVEL)
    file_handler.setFormatter(logging.Formatter(config.LOG_FORMATTER))

    return file_handler


def get_logger(name: str) -> logging.Logger:
    """
    Function to get logger.
    :param name: Logger name.
    """
    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)

    logger = logging.getLogger(name)
    logger.setLevel(config.TRACE_LEVEL)
    logger.addHandler(get_file_handler())

    return logger
