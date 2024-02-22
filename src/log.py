from collections.abc import Callable, Iterable
from functools import partial
import logging
from logging import Formatter, Handler, Logger
from typing import Any, Optional, TypeAlias

Level: TypeAlias = int
LoggerSetupFn: TypeAlias = Callable[[Logger], None]

_loggers: list[Logger] = []
_level: Level = logging.INFO
_handlers: list[Handler] = []

class LazyLogger:
    def __init__(self, factory: Callable[[], Logger], callbacks: Iterable[LoggerSetupFn]):
        self._logger = None
        self._factory = factory
        self._callbacks = callbacks

    def debug(self, template: str, *args: Any) -> None:
        if _level <= logging.DEBUG:
            self._get_or_create().debug(template, *args)

    def info(self, template: str, *args: Any) -> None:
        if _level <= logging.INFO:
            self._get_or_create().info(template, *args)

    def warn(self, template: str, *args: Any, exception: Optional[Exception] = None) -> None:
        if _level < logging.WARN:
            return
        logger = self._get_or_create()
        logger.warn(template, *args)
        if exception is not None:
            logger.exception(exception)

    def error(self, template: str, *args: Any, exception: Optional[Exception] = None) -> None:
        if _level < logging.ERROR:
            return
        logger = self._get_or_create()
        logger.error(template, *args)
        if exception is not None:
            logger.exception(exception)

    def critical(self, template: str, *args: Any, exception: Optional[Exception] = None) -> None:
        if _level < logging.CRITICAL:
            return
        logger = self._get_or_create()
        logger.critical(template, *args)
        if exception is not None:
            logger.exception(exception)

    def _get_or_create(self) -> Logger:
        if self._logger is None:
            self._logger = self._factory()
            _emit_callbacks(self._logger, self._callbacks)
        return self._logger

def _emit_callbacks(logger: Logger, callbacks: Iterable[LoggerSetupFn]):
    for callback in callbacks:
        callback(logger)

def add_formatter_to(formatter: Formatter, handlers: list[Handler]) -> None:
    for handler in handlers:
        handler.setFormatter(formatter)

def set_level(level: int) -> None:
    global _level
    _level = level
    for logger in _loggers:
        logger.setLevel(level)

def set_handlers(handlers: list[Handler]) -> None:
    global _handlers
    _handlers.extend(handlers)
    for logger in _loggers:
        for handler in handlers:
            logger.addHandler(handler)

def create_logger(name: str) -> LazyLogger:
    build_fn = partial(_build_logger, name)
    logger_setup = [
        _add_logger,
        _set_level,
        _set_handlers,
    ]
    return LazyLogger(build_fn, logger_setup)

def _build_logger(name: str) -> Logger:
    global _loggers
    logger = logging.getLogger(name)
    return logger

def _add_logger(logger: Logger) -> None:
    global _loggers
    _loggers.append(logger)

def _set_level(logger: Logger) -> None:
    logger.setLevel(_level)

def _set_handlers(logger: Logger) -> None:
    for handler in _handlers:
        logger.addHandler(handler)
