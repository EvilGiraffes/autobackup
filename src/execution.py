import shutil
from typing import Callable, TypeAlias, TYPE_CHECKING

import log

from main import ExitCode, InputFn

if TYPE_CHECKING:
    from pathlib import Path

logger = log.create_logger(__name__)

if TYPE_CHECKING: 
    ExecutionFn: TypeAlias = Callable[[Path, Path, InputFn], None]

def copy_tree(src: 'Path', dst: 'Path', input_fn: InputFn) -> None:
    try:
        shutil.copytree(src, dst)
    except FileExistsError:
        logger.info("folder already exists")
        given: str = input_fn()
        if given.lower() == "y":
            shutil.rmtree(dst)
            copy_tree(src, dst, input_fn)
            return
        else:
            logger.info("exiting...")
            exit(ExitCode.SUCCESS)

def zip(src: 'Path', dst: 'Path', input_fn: InputFn) -> None:
    raise NotImplemented("not implemented yet")
