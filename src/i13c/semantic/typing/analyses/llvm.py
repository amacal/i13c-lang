from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.core import Hex
from i13c.semantic.typing.analyses.asmlets import AsmletId
from i13c.semantic.typing.entities.functions import FunctionId


@dataclass(kw_only=True, repr=False)
class Immediate:
    value: Hex

    def width(self) -> Kind[8, 16, 32, 64]:
        return self.value.width

    def __str__(self) -> str:
        return str(self.value)


@dataclass(kw_only=True, repr=False)
class Register:
    name: bytes

    def __str__(self) -> str:
        return self.name.decode("utf-8")


class RegisterInfo:
    @staticmethod
    def derive32(name: bytes, width: Kind[8, 16, 32, 64]) -> Register:
        # fmt: off
        registers = {
            64: [b"rax", b"rbx", b"rcx", b"rdx", b"rsi", b"rdi", b"rsp", b"rbp", b"r8", b"r9", b"r10", b"r11", b"r12", b"r13", b"r14", b"r15"],
            32: [b"eax", b"ebx", b"ecx", b"edx", b"esi", b"edi", b"esp", b"ebp", b"r8d", b"r9d", b"r10d", b"r11d", b"r12d", b"r13d", b"r14d", b"r15d"],
            16: [b"ax", b"bx", b"cx", b"dx", b"si", b"di", b"sp", b"bp", b"r8w", b"r9w", b"r10w", b"r11w", b"r12w", b"r13w", b"r14w", b"r15w"],
            8: [b"al", b"bl", b"cl", b"dl", b"sil", b"dil", b"spl", b"bpl", b"r8b", b"r9b", b"r10b", b"r11b", b"r12b", b"r13b", b"r14b", b"r15b"],
        }
        # fmt: on

        # coerce derived width to at least 32 bits
        width = max(width, 32)

        return Register(name=registers[width][registers[64].index(name)])


class ImmediateInfo:
    @staticmethod
    def extend32(value: Hex, width: Kind[8, 16, 32, 64]) -> Immediate:
        # coerce derived width to at least 32 bits
        width = max(width, 32)

        if value.width < 32:
            value = value.extend(32)

        return Immediate(value=value)


@dataclass(kw_only=True, repr=False)
class Index:
    reg: Register
    scale: Kind[1, 2, 4, 8]

    def __str__(self) -> str:
        return f"{self.scale} * {self.reg}"


AddressSize = Kind[8, 16, 32, 64]
DisplacementWidth = Kind[0, 8, 32]
DisplacementDirection = Kind["forward", "backward"]
DisplacementOffset = bytes


@dataclass(kw_only=True, repr=False)
class Displacement:
    width: DisplacementWidth
    offset: DisplacementOffset
    direction: DisplacementDirection

    @staticmethod
    def positive(value: int) -> Displacement:
        data = value.to_bytes(4, "big")
        width = 8 if len(data.lstrip(bytes([0x00]))) <= 1 else 32

        if width == 8:
            data = data[-1:]

        return Displacement(
            width=width,
            offset=data,
            direction="forward",
        )

    def __str__(self) -> str:
        if self.direction == "forward":
            return f"+ 0x{self.offset.hex()}"
        else:
            return f"- 0x{self.offset.hex()}"


@dataclass(kw_only=True, repr=False)
class Address:
    size: AddressSize
    base: Register | None
    indx: Index | None
    disp: Displacement | None

    def __str__(self) -> str:
        repr: list[str] = []
        disp: str = ""

        match self.size:
            case 8:
                size = "byte"
            case 16:
                size = "word"
            case 32:
                size = "dword"
            case 64:
                size = "qword"

        if self.base is not None:
            repr.append(str(self.base))

        if self.indx is not None:
            repr.append(str(self.indx))

        if self.disp is not None:
            disp = str(self.disp)

        value = f"{' + '.join(repr)} {disp}"
        return f"{size} [{value.strip()}]"


@dataclass(kw_only=True, repr=False)
class Relocation:
    block: int

    def __str__(self) -> str:
        return f"#{self.block}"


@dataclass(kw_only=True, repr=False)
class Fixed:
    value: bytes

    def __str__(self) -> str:
        return f"0x{self.value.hex()}"


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
    operands: tuple[Register | Address, Register | Address]

    def __str__(self) -> str:
        return f"xchg {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class LEA:
    operands: tuple[Register, Address | Fixed]

    def __str__(self) -> str:
        return f"lea {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class SHR:
    operands: Group2Operands

    def __str__(self) -> str:
        return f"shr {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class SHL:
    operands: Group2Operands

    def __str__(self) -> str:
        return f"shl {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class SAR:
    operands: Group2Operands

    def __str__(self) -> str:
        return f"sar {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class SAL:
    operands: Group2Operands

    def __str__(self) -> str:
        return f"sal {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class ROL:
    operands: Group2Operands

    def __str__(self) -> str:
        return f"rol {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class ROR:
    operands: Group2Operands

    def __str__(self) -> str:
        return f"ror {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class RCL:
    operands: Group2Operands

    def __str__(self) -> str:
        return f"rcl {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class RCR:
    operands: Group2Operands

    def __str__(self) -> str:
        return f"rcr {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class ADD:
    operands: Group1Operands

    def __str__(self) -> str:
        return f"add {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class OR:
    operands: Group1Operands

    def __str__(self) -> str:
        return f"or {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class ADC:
    operands: Group1Operands

    def __str__(self) -> str:
        return f"adc {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class SBB:
    operands: Group1Operands

    def __str__(self) -> str:
        return f"sbb {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class AND:
    operands: Group1Operands

    def __str__(self) -> str:
        return f"and {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class SUB:
    operands: Group1Operands

    def __str__(self) -> str:
        return f"sub {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class XOR:
    operands: Group1Operands

    def __str__(self) -> str:
        return f"xor {self.operands[0]}, {self.operands[1]}"


@dataclass(kw_only=True, repr=False)
class CMP:
    operands: Group1Operands

    def __str__(self) -> str:
        return f"cmp {self.operands[0]}, {self.operands[1]}"


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
    operands: tuple[Address | Register | Immediate]

    def __str__(self) -> str:
        return f"push {self.operands[0]}"


@dataclass(kw_only=True, repr=False)
class POP:
    operands: tuple[Address | Register]

    def __str__(self) -> str:
        return f"pop {self.operands[0]}"


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


Group1Operands = tuple[Register | Address, Register | Address | Immediate]
Group1Instruction = ADD | AND | OR | SUB | ADC | SBB | XOR | CMP


Group2Operands = tuple[Register | Address, Register | Immediate]
Group2Instruction = SHR | SHL | SAR | SAL | ROL | ROR | RCL | RCR
