import logging
import os

from logging.handlers import RotatingFileHandler
from srt import config


def get_file_handler():
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


def get_logger(name):
    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)

    logger = logging.getLogger(name)
    logger.setLevel(config.TRACE_LEVEL)
    logger.addHandler(get_file_handler())

    return logger
