import logging

import log
import execution
from execution import ExecutionFn

_DEFAULT: ExecutionFn = execution.copy_tree

_LOGGER: logging.Logger = log.create_logger(__name__)
_registry: dict[str, ExecutionFn] = {}


def register(key: str, fn: ExecutionFn) -> None:
    global _registry
    _LOGGER.debug("setting the key %s to function %s", key, fn.__name__)
    _registry[key] = fn


def get_or_default(key: str) -> ExecutionFn:
    _LOGGER.debug("trying to access %s", key)
    return _registry.get(key, _DEFAULT)

