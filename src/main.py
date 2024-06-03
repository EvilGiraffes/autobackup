import logging
import sys
from pathlib import Path

import log
import factory
import execution
import process

LOG_LEVEL = logging.DEBUG
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
RMDIR_PROMPT = "destination already exists, do you wish to remove destination folder? (y/n): "

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

def ensure_arg(index: int, name: str):
    try:
        return sys.argv[index]
    except IndexError:
        process.WithCode.FAILED.log_critical(_logger, "failed to get arg %s", name).exit()

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
    _logger.info("trying to get %s strategy", strategy)
    func = factory.get_or_default(strategy)
    try:
        _logger.info("executing strategy...")
        func(src, dst, lambda _: False)
        process.WithCode.SUCCESS.log_exit_info(_logger).exit()
    except Exception as err:
        process.WithCode.FAILED.log_critical(_logger, "strategy failed", exception = err).exit()

if __name__ == "__main__":
    main()
