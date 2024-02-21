import logging
from logging import Formatter, Handler, Logger

_loggers: list[Logger] = []

def add_formatter_to(formatter: Formatter, handlers: list[Handler]) -> None:
    for handler in handlers:
        handler.setFormatter(formatter)

def set_level(level: int) -> None:
    for logger in _loggers:
        logger.setLevel(level)

def set_handlers(handlers: list[Handler]) -> None:
    for logger in _loggers:
        for handler in handlers:
            logger.addHandler(handler)

def create_logger(name: str) -> Logger:
    global _loggers
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    _loggers.append(logger)
    return logger

