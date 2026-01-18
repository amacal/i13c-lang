from dataclasses import dataclass
from typing import Union

from i13c.lowering.typing.flows import BlockId


@dataclass
class JumpTerminator:
    target: BlockId


@dataclass
class TrapTerminator:
    pass


@dataclass
class ExitTerminator:
    pass


Terminator = Union[JumpTerminator, TrapTerminator, ExitTerminator]
