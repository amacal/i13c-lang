from dataclasses import dataclass
from typing import Literal as Kind
from typing import Protocol

from i13c.encoding.core import UnreachableEncodingError
from i13c.semantic.typing.analyses import llvm

RegisterOrAddress = llvm.Register | llvm.Address
RegisterOrConstant = llvm.Register | int


# fmt: off
REGISTERS = {
    # 64-bit
    b"rax": 0, b"rcx": 1, b"rdx": 2, b"rbx": 3, b"rsp": 4, b"rbp": 5, b"rsi": 6, b"rdi": 7,
    b"r8": 8, b"r9": 9, b"r10": 10, b"r11": 11, b"r12": 12, b"r13": 13, b"r14": 14, b"r15": 15,

    # 32-bit
    b"eax": 0, b"ecx": 1, b"edx": 2, b"ebx": 3, b"esp": 4, b"ebp": 5, b"esi": 6, b"edi": 7,
    b"r8d": 8, b"r9d": 9, b"r10d": 10, b"r11d": 11, b"r12d": 12, b"r13d": 13, b"r14d": 14, b"r15d": 15,

    # 16-bit
    b"ax": 0, b"cx": 1, b"dx": 2, b"bx": 3, b"sp": 4, b"bp": 5, b"si": 6, b"di": 7,
    b"r8w": 8, b"r9w": 9, b"r10w": 10, b"r11w": 11, b"r12w": 12, b"r13w": 13, b"r14w": 14, b"r15w": 15,

    # 8-bit low
    b"al": 0, b"cl": 1, b"dl": 2, b"bl": 3, b"spl": 4, b"bpl": 5, b"sil": 6, b"dil": 7,
    b"r8b": 8, b"r9b": 9, b"r10b": 10, b"r11b": 11, b"r12b": 12, b"r13b": 13, b"r14b": 14, b"r15b": 15,

    # 8-bit high
    b"ah": 4, b"ch": 5, b"dh": 6, b"bh": 7,
}
# fmt: on


class DisplacementInfo:
    @staticmethod
    def width(disp: llvm.Displacement | None) -> int:
        if disp is None:
            return 0

        if len(disp.offset) == 1:
            if disp.offset[0] > 0x80:
                return 32

            if disp.offset[0] > 0x7F and disp.direction == "forward":
                return 32

        return disp.width

    @staticmethod
    def fixed(value: int, width: int) -> bytes:
        assert width in (8, 16, 32, 64)
        return value.to_bytes(width // 8, byteorder="big", signed=True)

    @staticmethod
    def normalize(disp: llvm.Displacement | None, width: int) -> bytes:
        if disp is None:
            return bytes(width // 8)

        data = disp.offset
        direction = disp.direction

        assert width in (8, 16, 32)
        assert 8 * len(data) <= width

        if direction == "backward":
            value = int.from_bytes(data, byteorder="big", signed=False)
            data = (-value).to_bytes(width // 8, byteorder="big", signed=True)

        else:
            value = int.from_bytes(data, byteorder="big", signed=False)
            data = value.to_bytes(width // 8, byteorder="big", signed=False)

        return data


class ImmediateInfo:
    @staticmethod
    def is_one(imm: llvm.Immediate) -> bool:
        return imm.value.width == 8 and imm.value.data == b"\x01"

    @staticmethod
    def get_width(imm: llvm.Immediate) -> int:
        return imm.value.width

    @staticmethod
    def fits_signed(imm: llvm.Immediate, width: int) -> bool:
        assert width in (8, 16, 32, 64)

        return (
            imm.value.width == width
            or imm.value.width < width
            and imm.value.highest_bit() == 0
        )

    @staticmethod
    def normalize(imm: llvm.Immediate, width: int) -> llvm.Immediate:
        assert width in (8, 16, 32, 64)
        assert imm.value.width <= width

        val = int.from_bytes(imm.value.data, byteorder="big", signed=False)
        hex = val.to_bytes(width // 8, byteorder="big", signed=False)

        return llvm.Immediate(value=llvm.Hex(data=hex, width=width))


class AddressInfo:
    @staticmethod
    def get_width(addr: llvm.Address) -> int:
        return addr.size

    @staticmethod
    def is_64bit(addr: llvm.Address) -> bool:
        return addr.size == 64

    @staticmethod
    def is_32bit(addr: llvm.Address) -> bool:
        return addr.size == 32

    @staticmethod
    def is_16bit(addr: llvm.Address) -> bool:
        return addr.size == 16

    @staticmethod
    def is_8bit(addr: llvm.Address) -> bool:
        return addr.size == 8


class RegisterInfo:
    @staticmethod
    def is_64bit(reg: llvm.Register) -> bool:
        # fmt: off
        return reg.name in (
            b"rax", b"rbx", b"rcx", b"rdx", b"rsi", b"rdi", b"rsp", b"rbp",
            b"r8", b"r9", b"r10", b"r11", b"r12", b"r13", b"r14", b"r15",
        )
        # fmt: on

    @staticmethod
    def is_32bit(reg: llvm.Register) -> bool:
        # fmt: off
        return reg.name in (
            b"eax", b"ebx", b"ecx", b"edx", b"esi", b"edi", b"esp", b"ebp",
            b"r8d", b"r9d", b"r10d", b"r11d", b"r12d", b"r13d", b"r14d", b"r15d",
        )
        # fmt: on

    @staticmethod
    def is_16bit(reg: llvm.Register) -> bool:
        # fmt: off
        return reg.name in (
            b"ax", b"bx", b"cx", b"dx", b"si", b"di", b"sp", b"bp",
            b"r8w", b"r9w", b"r10w", b"r11w", b"r12w", b"r13w", b"r14w", b"r15w",
        )
        # fmt: on

    @staticmethod
    def is_8bit(reg: llvm.Register) -> bool:
        # fmt: off
        return reg.name in (
            b"al", b"cl", b"dl", b"bl", b"spl", b"bpl", b"sil", b"dil",
            b"r8b", b"r9b", b"r10b", b"r11b", b"r12b", b"r13b", b"r14b", b"r15b",
            b"ah", b"ch", b"dh", b"bh",
        )
        # fmt: on

    @staticmethod
    def is_8bit_special(reg: llvm.Register) -> bool:
        return reg.name in (b"spl", b"bpl", b"sil", b"dil")

    @staticmethod
    def is_low8bit(reg: llvm.Register) -> bool:
        # fmt: off
        return reg.name in (
            b"al", b"bl", b"cl", b"dl", b"spl", b"bpl", b"sil", b"dil",
            b"r8b", b"r9b", b"r10b", b"r11b", b"r12b", b"r13b", b"r14b", b"r15b",
        )
        # fmt: on

    @staticmethod
    def is_acc(reg: llvm.Register) -> bool:
        return reg.name in (b"al", b"ax", b"eax", b"rax")

    @staticmethod
    def get_width(reg: llvm.Register) -> int:
        if RegisterInfo.is_64bit(reg):
            return 64

        if RegisterInfo.is_32bit(reg):
            return 32

        if RegisterInfo.is_16bit(reg):
            return 16

        return 8

    @staticmethod
    def low_3bits(reg: llvm.Register) -> int:
        return REGISTERS[reg.name] & 0x07

    @staticmethod
    def high_bit(reg: llvm.Register) -> bool:
        return REGISTERS[reg.name] >= 8


@dataclass(kw_only=True)
class ModRMEncoding:
    rex_h: int
    rex_x: int
    rex_b: int
    modrm_mod: int
    modrm_rm: int
    sib_scale: int
    sib_index: int
    sib_base: int
    disp_width: int
    disp_value: bytes

    @staticmethod
    def default() -> ModRMEncoding:
        return ModRMEncoding(
            rex_h=0x00,
            rex_x=0b0000,
            rex_b=0b0000,
            modrm_mod=0b00,
            modrm_rm=0b000,
            sib_scale=0b00,
            sib_index=0b000,
            sib_base=0b000,
            disp_width=0,
            disp_value=b"",
        )

    def is_sib_required(self) -> bool:
        return self.modrm_mod != 0b11 and self.modrm_rm == 0b100

    def is_disp_required(self) -> bool:
        return self.disp_width > 0


@dataclass(kw_only=True)
class ModRegEncoding:
    rex_h: int
    rex_w: int
    rex_r: int
    modrm_reg: int


@dataclass(kw_only=True)
class OpCodeEncoding:
    rex_h: int
    rex_w: int
    rex_b: int
    opcode_reg: int

    @staticmethod
    def default() -> OpCodeEncoding:
        return OpCodeEncoding(
            rex_h=0x00,
            rex_w=0b0000,
            rex_b=0b0000,
            opcode_reg=0b0000,
        )


@dataclass(kw_only=True)
class RexEncoding:
    h: int
    w: int
    r: int
    x: int
    b: int

    @staticmethod
    def default() -> RexEncoding:
        return RexEncoding(
            h=0x00,
            w=0b0000,
            r=0b0000,
            x=0b0000,
            b=0b0000,
        )

    def get_bits(self) -> int:
        return self.h | self.w | self.r | self.x | self.b

    def is_required(self) -> bool:
        return self.get_bits() > 0


class ModRegToRex(Protocol):
    rex_h: int
    rex_w: int
    rex_r: int
    modrm_reg: int


class ModRmToRex(Protocol):
    rex_h: int
    rex_x: int
    rex_b: int


class OpCodeToRex(Protocol):
    rex_h: int
    rex_w: int
    rex_b: int


@dataclass(kw_only=True)
class PrefixEncoding:
    operand_override: int

    @staticmethod
    def default() -> PrefixEncoding:
        return PrefixEncoding(
            operand_override=0x00,
        )


def encode_prefixes(target: RegisterOrAddress | llvm.Immediate) -> PrefixEncoding:
    is_16bit = False

    if isinstance(target, llvm.Register):
        is_16bit |= RegisterInfo.is_16bit(target)

    if isinstance(target, llvm.Immediate):
        is_16bit |= target.width() == 16

    if isinstance(target, llvm.Address):
        is_16bit |= AddressInfo.is_16bit(target)

    return PrefixEncoding(
        operand_override=(0x66 if is_16bit else 0x00),
    )


def encode_rex(
    target: RegisterOrAddress | None,
    /,
    modrm_reg: ModRegToRex | None = None,
    modrm_rm: ModRmToRex | None = None,
    opcode_reg: OpCodeToRex | None = None,
) -> RexEncoding:
    rex = RexEncoding.default()
    reg = isinstance(target, llvm.Register)
    mem = isinstance(target, llvm.Address)

    if target is not None:
        is_reg_64 = reg and RegisterInfo.is_64bit(target)
        is_mem_64 = mem and AddressInfo.is_64bit(target)

        if is_reg_64 or is_mem_64 or not mem and not reg:
            rex.w |= 0b1000
            rex.h |= 0x40

    if (
        reg
        and RegisterInfo.is_low8bit(target)
        and REGISTERS[target.name] in (4, 5, 6, 7)
    ):
        rex.h |= 0x40

    if modrm_reg is not None:
        rex.h |= modrm_reg.rex_h
        rex.r |= modrm_reg.rex_r

    if modrm_rm is not None:
        rex.h |= modrm_rm.rex_h
        rex.x |= modrm_rm.rex_x
        rex.b |= modrm_rm.rex_b

    if opcode_reg is not None:
        rex.h |= opcode_reg.rex_h
        rex.w |= opcode_reg.rex_w
        rex.b |= opcode_reg.rex_b

    if rex.get_bits():
        rex.h |= 0x40

    return rex


DefaultMode = Kind["64-bit", "32-bit"]


def encode_opcode_reg(
    reg: llvm.Register,
    /,
    mode: DefaultMode = "32-bit",
) -> OpCodeEncoding:
    return OpCodeEncoding(
        rex_h=0x00,
        rex_w=0b1000 if mode == "32-bit" and RegisterInfo.is_64bit(reg) else 0b0000,
        rex_b=0b0001 if RegisterInfo.high_bit(reg) else 0b0000,
        opcode_reg=RegisterInfo.low_3bits(reg),
    )


def encode_modrm_reg(reg: RegisterOrConstant) -> ModRegEncoding:
    if isinstance(reg, llvm.Register):
        return ModRegEncoding(
            rex_h=0x40 if RegisterInfo.is_8bit_special(reg) else 0x00,
            rex_w=0b1000 if RegisterInfo.is_64bit(reg) else 0b0000,
            rex_r=0b0100 if RegisterInfo.high_bit(reg) else 0b0000,
            modrm_reg=RegisterInfo.low_3bits(reg),
        )

    else:
        return ModRegEncoding(
            rex_h=0x00,
            rex_w=0b0000,
            rex_r=0b0000,
            modrm_reg=reg & 0x07,
        )


def encode_modrm_rm(rm: RegisterOrAddress) -> ModRMEncoding:
    encoding = ModRMEncoding.default()

    if isinstance(rm, llvm.Register):
        encoding.modrm_mod = 0b11
        encoding.modrm_rm = RegisterInfo.low_3bits(rm)
        encoding.rex_b = 0b0001 if RegisterInfo.high_bit(rm) else 0b0000

    elif isinstance(rm.disp, llvm.Relocation):
        encoding.modrm_mod = 0b00
        encoding.modrm_rm = 0b101
        encoding.disp_width = 4
        encoding.disp_value = DisplacementInfo.fixed(rm.disp.block, 32)

    else:
        is_rsp_r12 = RegisterInfo.low_3bits(rm.base) == 0b100 if rm.base else False
        is_rbp_r13 = RegisterInfo.low_3bits(rm.base) == 0b101 if rm.base else False

        # RSP cannot be used as index register
        if rm.indx and rm.indx.reg.name == b"rsp":
            raise UnreachableEncodingError()

        if not rm.base or rm.indx or is_rsp_r12:
            encoding.modrm_mod = 0b00
            encoding.modrm_rm = 0b100

            if rm.indx:
                encoding.sib_index = RegisterInfo.low_3bits(rm.indx.reg)
                encoding.sib_scale = [1, 2, 4, 8].index(rm.indx.scale)
                encoding.rex_x = (
                    0b0010 if RegisterInfo.high_bit(rm.indx.reg) else 0b0000
                )
            else:
                encoding.sib_index = 0b100
                encoding.sib_scale = 0b00

            if rm.base:
                encoding.sib_base = RegisterInfo.low_3bits(rm.base)
                encoding.rex_b = 0b0001 if RegisterInfo.high_bit(rm.base) else 0b0000
                encoding.disp_width = 0
            else:
                encoding.sib_base = 0b101
                encoding.disp_width = 4

        else:
            encoding.modrm_mod = 0b00
            encoding.modrm_rm = RegisterInfo.low_3bits(rm.base)
            encoding.rex_b = 0b0001 if RegisterInfo.high_bit(rm.base) else 0b0000
            encoding.disp_width = 0

        # RBP and R13 cannot be used as base register without displacement
        if is_rbp_r13 and encoding.disp_width == 0:
            encoding.modrm_mod = 0b01
            encoding.disp_width = 1

        if encoding.disp_width < DisplacementInfo.width(rm.disp) // 8:
            if DisplacementInfo.width(rm.disp) == 8:
                encoding.modrm_mod = 0b01
                encoding.disp_width = 1
            else:
                encoding.modrm_mod = 0b10
                encoding.disp_width = 4

        encoding.disp_value = DisplacementInfo.normalize(
            rm.disp, encoding.disp_width * 8
        )

    return encoding


def write_prefixes(bytecode: bytearray, prefixes: PrefixEncoding) -> None:
    if prefixes.operand_override:
        bytecode.append(prefixes.operand_override)


def write_rex(bytecode: bytearray, rex: RexEncoding) -> None:
    if rex.is_required():
        bytecode.append(rex.get_bits())


def write_modrm(
    bytecode: bytearray,
    modrm_reg: ModRegEncoding,
    modrm_rm: ModRMEncoding,
) -> None:

    # ModRM is always required
    bytecode.append(
        modrm_rm.modrm_mod << 6 | modrm_reg.modrm_reg << 3 | modrm_rm.modrm_rm
    )

    # SIB's presence is determined by ModRM encoding
    if modrm_rm.is_sib_required():
        bytecode.append(
            modrm_rm.sib_scale << 6 | modrm_rm.sib_index << 3 | modrm_rm.sib_base
        )

    # displacement is determined by ModRM encoding
    if modrm_rm.is_disp_required():
        bytecode.extend(reversed(modrm_rm.disp_value))


def write_opcode(
    bytecode: bytearray,
    opcode_length: int,
    opcode_value: int,
    /,
    opcode_reg: OpCodeEncoding | None = None,
) -> None:

    # append opcode register bits to opcode value if present
    if opcode_reg is not None:
        opcode_value |= opcode_reg.opcode_reg

    # opcode is blindly encoded as big-endian, because we human provide it this way
    bytecode.extend(opcode_value.to_bytes(opcode_length, byteorder="big", signed=False))


def write_immediate(
    bytecode: bytearray,
    imm: llvm.Immediate | None,
    /,
    condition: bool = True,
) -> None:
    if condition and imm is not None:
        bytecode.extend(reversed(imm.value.data))
