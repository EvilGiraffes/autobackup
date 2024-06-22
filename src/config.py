from pathlib import Path
import log

from argparse import ArgumentParser, Namespace

class Config:
    __slots__ = ("_namespace", "_default_log_level")
    
    def __init__(self, namespace: Namespace, default_log_level: log.Level) -> None:
        self._namespace = namespace
        self._default_log_level = default_log_level

    def src(self) -> Path:
        return self._namespace.src

    def dst(self) -> Path:
        return self._namespace.dst

    def force_yes(self) -> bool:
        return self._namespace.y

    def log_level(self) -> log.Level:
        def clamp(val: log.Level) -> log.Level:
            max = self._default_log_level // 10
            if val < 1:
                return 0
            if val > max:
                return max
            return val

        if self._default_log_level < 10:
            raise TypeError("The default has to be atleast Debug")
        return self._default_log_level - clamp(self._namespace.v) * 10


def setup(parser: ArgumentParser, default_log_level: log.Level) -> Config:
    assert default_log_level > 9, "Default level below nine will cause unforseen issues"
    parser.add_argument(
        "src",
        type=Path,
        help="The source folder to copy from"
    )
    parser.add_argument(
        "dst",
        type=Path,
        help="The destination folder to copy to"
    )
    parser.add_argument(
        "-v",
        default=0,
        action="count",
        help=f"The verbosity of the logging, max verbosity is -{'v' * (default_log_level // 10 - 1)}"
    )
    parser.add_argument(
        "-y", "-yes",
        action="store_true",
        help="Forces yes on all prompts"
    )
    return Config(parser.parse_args(), default_log_level)

