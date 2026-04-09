from dataclasses import dataclass
from typing import Union

from i13c.llvm.typing.instructions.core import Address, Immediate, Register
from i13c.llvm.typing.registers import reg64_to_name


@dataclass(kw_only=True)
class AddRegImm:
    dst: int
    imm: Immediate

    def native(self) -> str:
        return f"add {reg64_to_name(self.dst)}, {self.imm}"


@dataclass(kw_only=True)
class AddRegReg:
    dst: int
    src: int

    def native(self) -> str:
        return f"add {reg64_to_name(self.dst)}, {reg64_to_name(self.src)}"


@dataclass(kw_only=True)
class SUB:
    dst: Union[Register, Address]
    src: Union[Immediate, Register, Address]

    def native(self) -> str:
        return f"sub {self.dst}, {self.src}"
