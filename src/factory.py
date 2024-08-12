import logging
from typing import Iterable

import log
from execution import ExecutionFn

_LOGGER: logging.Logger = log.create_logger(__name__)
_registry: dict[str, ExecutionFn] = {}


def set_registry(registry: dict[str, ExecutionFn]) -> None:
    global _registry
    _LOGGER.debug("setting the registry to %s", registry)
    _registry = registry


def get(key: str) -> ExecutionFn:
    return _registry[key]


def strategy_names() -> Iterable[str]:
    return _registry.keys()

