import shutil
import logging
import sys
from typing import Callable, TypeAlias 
from pathlib import Path

LOG_LEVEL = logging.DEBUG
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
RMDIR_PROMPT = "destination already exists, do you wish to remove destination folder?"

InputFn: TypeAlias = Callable[[str], str]

logger: logging.Logger = logging.getLogger("main")

def Ignore_with_log(src: Path, dst: Path, *, follow_symlinks: bool = True) -> None:
    logger.debug("copying from %s to %s", src, dst)
    logger.debug("following symlinks is %s", follow_symlinks)
    try:
        shutil.copy2(src, dst, follow_symlinks = follow_symlinks)
    except Exception as err:
        logger.warn("failed to copy from %s to %s: %s", src, dst, err)

def ensure_arg(index: int, name: str):
    try:
        return sys.argv[index]
    except IndexError:
        logger.critical(f"not given {name}")
        sys.exit(1)

def to_flag(given: str) -> bool:
    given_lower = given.lower()
    if given_lower == "-y":
        return True
    else:
        return False

def create_flagged_input(skip: bool) -> InputFn:
    def flagged_input(prompt: str) -> str:
        if skip:
            logger.debug("skipping prompt")
            return "y"
        return input(prompt)
    return flagged_input

def execute(src: Path, dst: Path, input_fn: InputFn) -> None:
    try:
        shutil.copytree(src, dst)
    except FileExistsError:
        logger.info("folder already exists")
        given: str = input_fn(f"{RMDIR_PROMPT} (y/n): ")
        if given.lower() == "y":
            shutil.rmtree(dst)
            execute(src, dst, input_fn)
            return
        else:
            logger.info("exiting...")
            sys.exit(0)

def main():
    # setup logger handling
    formatter = logging.Formatter(FORMAT)
    file_handler = logging.FileHandler("health.log")
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # setup logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(LOG_LEVEL)

    # get the source and destination
    src = Path(ensure_arg(1, "source"))
    dst = Path(ensure_arg(2, "destination"))
    logger.debug("src is %s and dst is %s", src, dst)
    if len(sys.argv) >= 4:
        logging.debug("is flagged input")
        input_fn = create_flagged_input(
            to_flag(sys.argv[3])
        )
    else:
        logging.debug("is not flagged input")
        input_fn = input

    execute(src, dst, input_fn)

if __name__ == "__main__":
    main()
