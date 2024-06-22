import logging

import log
from execution import ExecutionFn

_LOGGER: logging.Logger = log.create_logger(__name__)
_registry: dict[str, ExecutionFn] = {}

def set_registry(registry: dict[str, ExecutionFn]) -> None:
    global _registry
    _LOGGER.debug("setting the registry to %s", registry)
    _registry = registry

def try_get(key: str) -> ExecutionFn | None:
    _LOGGER.debug("trying to access %s", key)
    return _registry.get(key)
