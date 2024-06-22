import logging
import sys
from argparse import ArgumentParser

import log
import factory
import execution
import config

# Program info

NAME = "ba"
DESCRIPTION = "Does a backup from source to a destination folder automatically"

# Logging config

FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DEFAULT_LEVEL = logging.WARNING

_LOGGER: log.LazyLogger = log.create_logger(__name__)

def setup_logger(level: log.Level) -> None:
    global _LOGGER
    # setup logger handling
    formatter = logging.Formatter(FORMAT)
    handlers = [
        logging.FileHandler("../health.log"),
        logging.StreamHandler(sys.stdout),
    ]
    log.add_formatter_to(formatter, handlers)

    # setup logger
    log.set_level(level)
    log.add_handlers(handlers)

def input_continuation(prompt: str) -> bool:
    while True:
        given = input(f"{prompt} (y/n): ").lower()
        if given in ("y", "yes"):
            return True
        elif given in ("n", "no"):
            return False
        else:
            print(f"Incorrect input got {given}, did you mean \"no?\"")

def main():
    data = config.setup(
        ArgumentParser(
            prog=NAME,
            description=DESCRIPTION,
        ),
        DEFAULT_LEVEL
    )
    print(data.log_level())
    setup_logger(data.log_level())
    _LOGGER.info("program start")
    # register strategies
    strategies = [
        ("copy", execution.copy_tree),
        ("zip", execution.zip),
    ]
    _LOGGER.info("registering strategies")
    for (key, fn) in strategies:
        factory.register(key, fn)

    strategy = "copy" #TODO get from args

    # get the source and destination
    src = data.src()
    dst = data.dst()
    _LOGGER.debug("src is %s and dst is %s", src, dst)
    _LOGGER.info("trying to get %s strategy", strategy)
    func = factory.get_or_default(strategy)
    if data.force_yes():
        continuation_fn = lambda _: True
    else:
        continuation_fn = input_continuation
    _LOGGER.info("executing strategy...")
    exitcode = func(src, dst, continuation_fn)
    exit(exitcode)


if __name__ == "__main__":
    main()
