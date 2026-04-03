from dataclasses import dataclass
from typing import Union

from i13c.llvm.typing.instructions.core import Address, Register


@dataclass(kw_only=True)
class LeaReg32Mem:
    dst: Register
    addr: Address

    def native(self) -> str:
        return f"lea {self.dst}, {self.addr}"


@dataclass(kw_only=True)
class LeaReg64Mem:
    dst: Register
    addr: Address

    def native(self) -> str:
        return f"lea {self.dst}, {self.addr}"


LeaInstruction = Union[LeaReg32Mem, LeaReg64Mem]
