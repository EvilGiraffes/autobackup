import shutil
from typing import Callable, TypeAlias
from pathlib import Path

import log

_logger: log.LazyLogger = log.create_logger(__name__)

# TODO remove InputFn as a param
Continue: TypeAlias = bool
ErrorHandler: TypeAlias = Callable[[Exception], Continue]
ExecutionFn: TypeAlias = Callable[[Path, Path, ErrorHandler], None]

def copy_tree(src: Path, dst: Path, error_handler: ErrorHandler) -> None:
    try:
        shutil.copytree(src, dst, copy_function = _ignore_with_log)
    except FileExistsError as err:
        _logger.info("folder already exists")
        if error_handler(err):
            shutil.rmtree(dst)
            copy_tree(src, dst, error_handler)
            return
        else:
            _logger.error("file at location %s already exists", dst, exception = err)
            raise

def zip(src: Path, dst: Path, error_handler: ErrorHandler) -> None:
    raise NotImplemented("not implemented yet")

def _ignore_with_log(src: str, dst: str, *, follow_symlinks: bool = True) -> shutil._PathReturn:
    _logger.debug("copying from %s to %s", src, dst)
    _logger.debug("following symlinks is %s", follow_symlinks)
    try:
        return shutil.copy2(src, dst, follow_symlinks = follow_symlinks)
    except OSError as err:
        _logger.warn("failed to copy from %s to %s: %s", src, dst, exception = err)
