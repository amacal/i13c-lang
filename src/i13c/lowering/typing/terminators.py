from dataclasses import dataclass
from typing import Union

from i13c.lowering.typing.flows import BlockId


@dataclass
class JumpTerminator:
    target: BlockId

    def __str__(self) -> str:
        return f"Jump({self.target.identify(1)})"


@dataclass
class TrapTerminator:
    def __str__(self) -> str:
        return "Trap"


@dataclass
class ExitTerminator:
    def __str__(self) -> str:
        return "Exit"


Terminator = Union[JumpTerminator, TrapTerminator, ExitTerminator]
