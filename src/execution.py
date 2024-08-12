import logging
import shutil
from typing import Any, Callable, TypeAlias
from pathlib import Path

import log

_LOGGER: logging.Logger = log.create_logger(__name__)

ExitCode: TypeAlias = int
ContinuationFn: TypeAlias = Callable[[str], bool]
ExecutionFn: TypeAlias = Callable[[Path, Path, ContinuationFn], ExitCode]

def copy_tree(src: Path, dst: Path, continuation_fn: ContinuationFn) -> ExitCode:
    _LOGGER.info("Trying to copy directory %s to %s", src, dst)
    try:
        shutil.copytree(src, dst, copy_function = _ignore_with_log)
    except FileExistsError:
        _LOGGER.info("folder already exists")
        if continuation_fn("destination already exists, do you wish to overwrite folder?"):
            shutil.rmtree(dst)
            return copy_tree(src, dst, continuation_fn)
        else:
            return 1
    except FileNotFoundError:
        msg = "Cannot find folder %s"
        if src.is_absolute():
            _LOGGER.critical(msg, src)
        else:
            _LOGGER.critical(msg + " [%s]", src, src.absolute())
        return 1

    return 0

def zip(src: Path, dst: Path, continuation_fn: ContinuationFn) -> ExitCode:
    raise NotImplementedError("not implemented yet")

def _ignore_with_log(src: str, dst: str, *, follow_symlinks: bool = True) -> Any:
    _LOGGER.info("trying to copying file %s to %s", src, dst)
    try:
        res = shutil.copy2(src, dst, follow_symlinks = follow_symlinks)
        _LOGGER.debug("copy succeeded")
        return res
    except OSError:
        _LOGGER.warn("copy failed: ", exc_info=True)
