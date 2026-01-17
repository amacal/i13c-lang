from dataclasses import dataclass
from typing import Union


@dataclass
class FallThroughTerminator:
    pass


@dataclass
class TrapTerminator:
    pass


@dataclass
class ExitTerminator:
    pass


Terminator = Union[FallThroughTerminator, TrapTerminator, ExitTerminator]
