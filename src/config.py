from pathlib import Path
from argparse import ArgumentParser
from dataclasses import dataclass

import factory


@dataclass(frozen=True, slots=True)
class Config:
    src: Path
    dst: Path
    strategy: str
    verbosity: int
    force_yes: bool


def setup(parser: ArgumentParser, max_log_verbosity: int) -> Config:
    parser.add_argument(
        "src",
        type=Path,
        help="The source folder to copy from",
    )
    parser.add_argument(
        "dst",
        type=Path,
        help="The destination folder to copy to",
    )
    parser.add_argument(
        "-s", "--strategy",
        choices=factory.strategy_names(),
        help="The strategy to use when doing a backup"
    )
    parser.add_argument(
        "-v",
        default=0,
        action="count",
        help=f"The verbosity of the logging, max verbosity is -{'v' * max_log_verbosity}",
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Forces yes on all prompts",
    )

    namespace = parser.parse_args()

    return Config(
        src=namespace.src,
        dst=namespace.dst,
        strategy=namespace.strategy,
        verbosity=namespace.v,
        force_yes=namespace.yes,
    )
