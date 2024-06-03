import logging
from pathlib import Path
import log

from argparse import ArgumentParser, Namespace

class Config:
    __slots__ = ("_namespace")
    
    def __init__(self, namespace: Namespace) -> None:
        self._namespace = namespace

    def src(self) -> Path:
        return self._namespace.src

    def dst(self) -> Path:
        return self._namespace.dst

    def force_yes(self) -> bool:
        return self._namespace.y

    def log_level(self, default: log.Level) -> log.Level:
        if self._namespace.force_debug:
            return logging.DEBUG
        if default < 1:
            raise TypeError("The default has to be atleast Debug")
        verbosity = self._namespace.v
        if verbosity is None:
            return default
        max = default // 10 - 1
        if verbosity > max:
            return logging.DEBUG
        if verbosity >= default:
            return default
        return default - verbosity * 10

def setup(name: str, desc: str, epilog: str) -> Config:
    parser = ArgumentParser(
        prog=name,
        description=desc,
        epilog=epilog,
    )
    parser.add_argument("src", type=Path, help="The source folder to copy from")
    parser.add_argument("dst", type=Path, help="The destination folder to copy to")
    parser.add_argument("-v", action="count", help="The verbosity of the logging")
    parser.add_argument(
        "-d", "--force-debug", 
        action="store_true",
        help="Forces the program to log in debug mode, incase verbosity does not work"
    )
    parser.add_argument("-y", "-yes", action="store_true", help="Forces yes on all prompts")
    return Config(parser.parse_args())
