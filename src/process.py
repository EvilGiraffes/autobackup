from collections.abc import Callable
from functools import partial
from typing import NoReturn, Optional, Self, TypeAlias
from dataclasses import dataclass, field

from log import LazyLogger 

ExitingCallback: TypeAlias = Callable[[], None]

@dataclass
class _ExitCode:
    _code: int
    _callback: Optional[ExitingCallback] = field(default = None, init = False)

    def log_exit_info(self, logger: LazyLogger) -> Self:
        return self.with_callback(partial(logger.info, "exiting..."))

    def log_critical(
            self,
            logger: LazyLogger,
            template: str,
            *args,
            exception: Optional[Exception] = None
        ) -> Self:
        return self.with_callback(partial(logger.critical, template, *args, exception = exception))

    def with_callback(self, callback: ExitingCallback) -> Self:
        self._callback = callback
        return self

    def exit(self) -> NoReturn:
        if self._callback:
            self._callback()
        exit(self._code)

class WithCode:
    SUCCESS: _ExitCode = _ExitCode(0) 
    FAILED: _ExitCode = _ExitCode(1) 

