from dataclasses import dataclass

from i13c.semantic.core import Hex
from i13c.semantic.typing.analyses.asmlets import AsmletId
from i13c.semantic.typing.entities.functions import FunctionId


@dataclass(kw_only=True, repr=False)
class Immediate:
    value: Hex

    def __str__(self) -> str:
        return str(self.value)


@dataclass(kw_only=True, repr=False)
class Register:
    name: bytes

    def __str__(self) -> str:
        return self.name.decode("utf-8")


@dataclass(kw_only=True, repr=False)
class Address:
    base: Register
    disp: Hex | None

    def __str__(self) -> str:
        if self.disp is None:
            return f"[{self.base}]"
        else:
            return f"[{self.base} + {self.disp}]"


@dataclass(kw_only=True, repr=False)
class Relocation:
    block: int

    def __str__(self) -> str:
        return f"#{self.block}"


@dataclass(kw_only=True, repr=False)
class MOV:
    operands: tuple[Register | Address, Immediate | Register | Address]

    def __str__(self) -> str:
        return f"mov {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class BSWAP:
    operands: tuple[Register]

    def __str__(self) -> str:
        return f"bswap {self.operands[0]}"


@dataclass(kw_only=True, repr=False)
class XCHG:
    operands: tuple[Register, Register]

    def __str__(self) -> str:
        return f"xchg {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class LEA:
    operands: tuple[Register, Address]

    def __str__(self) -> str:
        return f"lea {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class SHR:
    operands: tuple[Register, Register | Immediate]

    def __str__(self) -> str:
        return f"shr {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class SHL:
    operands: tuple[Register, Register | Immediate]

    def __str__(self) -> str:
        return f"shl {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class AND:
    operands: tuple[Register, Register | Immediate]

    def __str__(self) -> str:
        return f"and {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class OR:
    operands: tuple[Register, Register | Immediate]

    def __str__(self) -> str:
        return f"or {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class NOP:
    def __str__(self) -> str:
        return "nop"


@dataclass(kw_only=True, repr=False)
class LOOP:
    operands: tuple[Relocation]

    def __str__(self) -> str:
        return f"loop {self.operands[0]}"


@dataclass(kw_only=True, repr=False)
class JMP:
    operands: tuple[Relocation]

    def __str__(self) -> str:
        return f"jmp {self.operands[0]}"


@dataclass(kw_only=True, repr=False)
class PUSH:
    operands: tuple[Register | Address]

    def __str__(self) -> str:
        return f"push {self.operands[0]}"


@dataclass(kw_only=True, repr=False)
class POP:
    operands: tuple[Register | Address]

    def __str__(self) -> str:
        return f"pop {self.operands[0]}"


@dataclass(kw_only=True, repr=False)
class ADD:
    operands: tuple[Register, Register | Immediate]

    def __str__(self) -> str:
        return f"add {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class SUB:
    operands: tuple[Register, Register | Immediate]

    def __str__(self) -> str:
        return f"sub {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class CALL:
    target: AsmletId | FunctionId

    def __str__(self) -> str:
        return f"call {self.target.identify(1)}"


@dataclass(kw_only=True, repr=False)
class RET:
    def __str__(self) -> str:
        return "ret"


@dataclass(kw_only=True, repr=False)
class SYSCALL:
    def __str__(self) -> str:
        return "syscall"
