import logging
from logging import Formatter, Handler, Logger
from typing import Callable, Iterable, TypeAlias

Level: TypeAlias = int
LoggerSetupFn: TypeAlias = Callable[[Logger], None]

_setup: LoggerSetupFn | None = None


def setup(func: LoggerSetupFn) -> None:
    global _setup
    _setup = func
    _setup(logging.root)


def add_formatter_to(formatter: Formatter, handlers: Iterable[Handler]) -> None:
    for handler in handlers:
        handler.setFormatter(formatter)


def add_handlers_to(logger: Logger, handlers: Iterable[Handler]):
    for handler in handlers:
        logger.addHandler(handler)


def create_logger(name: str) -> Logger:
    logger = logging.getLogger(name)
    if _setup:
        _setup(logger)
    return logger


def clamp_verbosity(verbosity: int, *, min: Level = logging.DEBUG, max: Level = logging.CRITICAL) -> int:
    def clamp(val: int, min: int, max: int) -> int:
        if val > max:
            return max
        if val < min:
            return min
        return val

    return clamp(verbosity, min // 10, max // 10)


def calculate_level(verbosity: int, default_level: Level, min: Level = logging.DEBUG) -> Level:
    if verbosity < min // 10:
        return min

    verbosity = clamp_verbosity(verbosity, max=default_level)
    return default_level - verbosity * 10 + 10
