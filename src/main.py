import logging
import sys
from argparse import ArgumentParser

import log
import factory
import execution
import config

# Program info

NAME: str = "ba"
DESCRIPTION: str = "Does a backup from source to a destination folder automatically"

# Logging config

FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"
DEFAULT_LEVEL: log.Level = logging.WARNING


DEFAULT_EXECUTION_FN: execution.ExecutionFn = execution.copy_tree
_LOGGER: logging.Logger = log.create_logger(__name__)


def logger_setup(level: log.Level) -> None:
    print(level)
    formatter = logging.Formatter(FORMAT)
    handlers = [
        logging.FileHandler("../health.log"),
        logging.StreamHandler(sys.stdout),
    ]
    log.add_formatter_to(formatter, handlers)

    def setup(logger: logging.Logger) -> None:
        nonlocal handlers
        logger.setLevel(level)
        log.add_handlers_to(logger, handlers)

    log.setup(setup)


def input_continuation(prompt: str) -> bool:
    while True:
        given = input(f"{prompt} (y/n): ").lower()
        if given in ("y", "yes"):
            return True
        elif given in ("n", "no"):
            return False
        else:
            print(f"Incorrect input got {given}, did you mean \"no?\"")


def always_true_continuation(_: str) -> bool:
    return True


def main() -> None:
    assert DEFAULT_LEVEL >= 10, "Default level below 10 can cause unforseen issues"
    assert (DEFAULT_LEVEL / 10).is_integer(), "Default level must be divisable by 10"

    strategies = {
        "copy": execution.copy_tree,
        "zip": execution.zip,
    }
    factory.set_registry(strategies)

    data = config.setup(
        ArgumentParser(
            prog=NAME,
            description=DESCRIPTION,
        ),
        DEFAULT_LEVEL // 10
    )

    logger_setup(log.calculate_level(data.verbosity, DEFAULT_LEVEL))

    _LOGGER.info("program start")

    strategy = data.strategy
    func: execution.ExecutionFn
    if strategy is None:
        _LOGGER.debug("No strategy given")
        func = DEFAULT_EXECUTION_FN
    else:
        func = factory.get(strategy)  # type: ignore
    if data.force_yes:
        continuation_fn = always_true_continuation
    else:
        continuation_fn = input_continuation

    _LOGGER.info("executing strategy...")
    exitcode = func(data.src, data.dst, continuation_fn)
    exit(exitcode)


if __name__ == "__main__":
    main()
