import shutil
import logging
import sys
from typing import Callable, TypeAlias 
from pathlib import Path
from functools import partial

import log
import factory
import execution
import process

LOG_LEVEL = logging.DEBUG
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
RMDIR_PROMPT = "destination already exists, do you wish to remove destination folder? (y/n): "

class ExitCode:
    SUCCESS = 0
    FAILED = 1

InputFn: TypeAlias = Callable[[], str]

# Will be initialized in main
_logger: log.LazyLogger = None # type: ignore

def setup_logger() -> None:
    global _logger
    # setup logger handling
    formatter = logging.Formatter(FORMAT)
    handlers = [
        logging.FileHandler("health.log"),
        logging.StreamHandler(sys.stdout),
    ]
    log.add_formatter_to(formatter, handlers)

    # setup logger
    log.set_level(LOG_LEVEL)
    log.add_handlers(handlers)
    _logger = log.create_logger(__name__)

def Ignore_with_log(src: Path, dst: Path, *, follow_symlinks: bool = True) -> None:
    _logger.debug("copying from %s to %s", src, dst)
    _logger.debug("following symlinks is %s", follow_symlinks)
    try:
        shutil.copy2(src, dst, follow_symlinks = follow_symlinks)
    except Exception as err:
        _logger.warn("failed to copy from %s to %s: %s", src, dst, exception = err)

def ensure_arg(index: int, name: str):
    try:
        return sys.argv[index]
    except IndexError:

def to_flag(given: str) -> bool:
    given_lower = given.lower()
    if given_lower == "-y":
        return True
    else:
        return False
        process.WithCode.FAILED.log_critical(_logger, "failed to get arg %s", name).exit()

def create_flagged_input(skip: bool) -> InputFn:
    def flagged_input() -> str:
        if skip:
            _logger.debug("skipping prompt")
            return "y"
        return input(RMDIR_PROMPT)
    return flagged_input

def main():
    setup_logger()
    _logger.info("program start")
    # register strategies
    strategies = [
        ("copy", execution.copy_tree),
        ("zip", execution.zip),
    ]
    _logger.info("registering strategies")
    for (key, fn) in strategies:
        factory.register(key, fn)

    strategy = "copy" #TODO get from args

    # get the source and destination
    src = Path(ensure_arg(1, "source"))
    dst = Path(ensure_arg(2, "destination"))
    _logger.debug("src is %s and dst is %s", src, dst)
    if len(sys.argv) >= 4:
        logging.debug("is flagged input")
        input_fn = create_flagged_input(
            to_flag(sys.argv[3])
        )
    else:
        logging.debug("is not flagged input")
        input_fn = partial(input, RMDIR_PROMPT)

    func = factory.get_or_default("copy")
    _logger.info("trying to get %s strategy", strategy)
    func = factory.get_or_default(strategy)
    try:
        _logger.info("executing strategy...")
        func(src, dst, noop_error_handler)
        process.WithCode.SUCCESS.log_exit_info(_logger).exit()
    except Exception as err:
        process.WithCode.FAILED.log_critical(_logger, "strategy failed", exception = err).exit()

if __name__ == "__main__":
    main()
