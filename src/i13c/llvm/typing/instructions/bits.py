from dataclasses import dataclass
from typing import Union

from i13c.llvm.typing.instructions.core import Immediate, Register


@dataclass(kw_only=True)
class BSWAP:
    dst: Register

    def native(self) -> str:
        return f"bswap {self.dst}"


@dataclass(kw_only=True)
class SHL:
    dst: Register
    src: Union[Immediate, Register]

    def native(self) -> str:
        return f"shl {self.dst}, {self.src}"
