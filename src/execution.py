import shutil
from typing import Any, Callable, TypeAlias
from pathlib import Path

import log

_LOGGER: log.LazyLogger = log.create_logger(__name__)

ContinuationFn: TypeAlias = Callable[[str], bool]
ExecutionFn: TypeAlias = Callable[[Path, Path, ContinuationFn], None]

def copy_tree(src: Path, dst: Path, continuation_fn: ContinuationFn) -> None:
    try:
        shutil.copytree(src, dst, copy_function = _ignore_with_log)
    except FileExistsError as err:
        _LOGGER.info("folder already exists")
        if continuation_fn("destination already exists, do you wish to remove destination folder?"):
            shutil.rmtree(dst)
            copy_tree(src, dst, continuation_fn)
            return
        else:
            _LOGGER.error("file at location %s already exists", dst, exception = err)
            raise

def zip(src: Path, dst: Path, continuation_fn: ContinuationFn) -> None:
    raise NotImplemented("not implemented yet")

def _ignore_with_log(src: str, dst: str, *, follow_symlinks: bool = True) -> Any:
    _LOGGER.debug("copying from %s to %s", src, dst)
    _LOGGER.debug("following symlinks is %s", follow_symlinks)
    try:
        return shutil.copy2(src, dst, follow_symlinks = follow_symlinks)
    except OSError as err:
        _LOGGER.warn("failed to copy from %s to %s: %s", src, dst, exception = err)
