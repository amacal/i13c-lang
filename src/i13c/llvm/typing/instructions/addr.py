from dataclasses import dataclass

from i13c.llvm.typing.instructions.core import Address, Register


@dataclass(kw_only=True)
class LEA:
    dst: Register
    src: Address

    def native(self) -> str:
        return f"lea {self.dst}, {self.src}"
