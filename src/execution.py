import shutil
from typing import Callable, TypeAlias
from pathlib import Path

import log

from main import ExitCode, InputFn

_logger: log.LazyLogger = log.create_logger(__name__)

# TODO remove InputFn as a param
ExecutionFn: TypeAlias = Callable[[Path, Path, InputFn], None]

def copy_tree(src: 'Path', dst: 'Path', input_fn: InputFn) -> None:
    try:
        shutil.copytree(src, dst)
    except FileExistsError:
        _logger.info("folder already exists")
        given: str = input_fn()
        if given.lower() == "y":
            shutil.rmtree(dst)
            copy_tree(src, dst, input_fn)
            return
        else:
            _logger.info("exiting...")
            exit(ExitCode.SUCCESS)

def zip(src: 'Path', dst: 'Path', input_fn: InputFn) -> None:
    raise NotImplemented("not implemented yet")
