import logging
from logging import Formatter, Handler, Logger
from typing import Callable, Iterator, TypeAlias

Level: TypeAlias = int
LoggerSetupFn: TypeAlias = Callable[[Logger], None]

_setup: LoggerSetupFn | None = None

def setup(func: LoggerSetupFn) -> None:
    global _setup
    _setup = func
    _setup(logging.root)


def add_formatter_to(formatter: Formatter, handlers: Iterator[Handler]) -> None:
    for handler in handlers:
        handler.setFormatter(formatter)


def add_handlers_to(logger: Logger, handlers: Iterator[Handler]):
    for handler in handlers:
        logger.addHandler(handler)


def create_logger(name: str) -> Logger:
    logger = logging.getLogger(name)
    if _setup:
        _setup(logger)
    return logger

