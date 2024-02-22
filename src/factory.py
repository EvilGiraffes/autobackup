import execution

import log

from execution import ExecutionFn

_DEFAULT: 'ExecutionFn' = execution.copy_tree

_logger: log.LazyLogger = log.create_logger(__name__)
_registry: dict[str, 'ExecutionFn'] = {}

def register(key: str, fn: 'ExecutionFn') -> None:
    global _registry
    _logger.debug("setting the key %s to function %s", key, fn)
    _registry[key] = fn

def get_or_default(key: str) -> 'ExecutionFn':
    _logger.debug("trying to access %s, currently got %s", key, _registry)
    return _registry.get(key, _DEFAULT)

