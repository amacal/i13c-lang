from dataclasses import dataclass
from typing import Optional, Protocol, Union

from i13c.encoding.core import UnreachableEncodingError
from i13c.llvm.typing.instructions import core as llvm

RegisterOrAddress = Union[llvm.Register, llvm.ComputedAddress, llvm.RelativeAddress]
RegisterOrConstant = Union[llvm.Register, int]


@dataclass(kw_only=True)
class ModRMEncoding:
    rex_x: int
    rex_b: int
    modrm_mod: int
    modrm_rm: int
    sib_scale: int
    sib_index: int
    sib_base: int
    disp_width: int
    disp_value: int

    @staticmethod
    def default() -> ModRMEncoding:
        return ModRMEncoding(
            rex_x=0b0000,
            rex_b=0b0000,
            modrm_mod=0b00,
            modrm_rm=0b000,
            sib_scale=0b00,
            sib_index=0b000,
            sib_base=0b000,
            disp_width=0,
            disp_value=0,
        )

    def is_sib_required(self) -> bool:
        return self.modrm_mod != 0b11 and self.modrm_rm == 0b100

    def is_disp_required(self) -> bool:
        return self.disp_width > 0


@dataclass(kw_only=True)
class ModRegEncoding:
    rex_w: int
    rex_r: int
    modrm_reg: int


@dataclass(kw_only=True)
class OpCodeEncoding:
    rex_w: int
    rex_b: int
    opcode_reg: int


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
    rex_w: int
    rex_r: int
    modrm_reg: int


class ModRmToRex(Protocol):
    rex_x: int
    rex_b: int


class OpCodeToRex(Protocol):
    rex_w: int
    rex_b: int


@dataclass(kw_only=True)
class PrefixEncoding:
    operand_override: int


def encode_prefixes(instruction: llvm.Register) -> PrefixEncoding:
    return PrefixEncoding(
        operand_override=0x66 if instruction.is_16bit() else 0x00,
    )


def encode_rex(
    reg: llvm.Register,
    /,
    modrm_reg: Optional[ModRegToRex] = None,
    modrm_rm: Optional[ModRmToRex] = None,
    opcode_reg: Optional[OpCodeToRex] = None,
) -> RexEncoding:
    rex = RexEncoding.default()

    if reg.is_64bit():
        rex.w |= 0b1000
        rex.h |= 0x40

    if reg.is_low8bit() and reg.id in (4, 5, 6, 7):
        rex.h |= 0x40

    if modrm_reg is not None:
        rex.r |= modrm_reg.rex_r

    if modrm_rm is not None:
        rex.x |= modrm_rm.rex_x
        rex.b |= modrm_rm.rex_b

    if opcode_reg is not None:
        rex.w |= opcode_reg.rex_w
        rex.b |= opcode_reg.rex_b

    if rex.get_bits():
        rex.h |= 0x40

    return rex


def encode_opcode_reg(reg: llvm.Register) -> OpCodeEncoding:
    return OpCodeEncoding(
        rex_w=0b1000 if reg.is_64bit() else 0b0000,
        rex_b=0b0001 if reg.high_bit() else 0b0000,
        opcode_reg=reg.low3bits(),
    )


def encode_modrm_reg(reg: RegisterOrConstant) -> ModRegEncoding:
    if isinstance(reg, llvm.Register):
        return ModRegEncoding(
            rex_w=0b1000 if reg.is_64bit() else 0b0000,
            rex_r=0b0100 if reg.high_bit() else 0b0000,
            modrm_reg=reg.low3bits(),
        )

    return ModRegEncoding(
        rex_w=0b0000,
        rex_r=0b0000,
        modrm_reg=reg & 0x07,
    )


def encode_modrm_rm(rm: RegisterOrAddress) -> ModRMEncoding:
    encoding = ModRMEncoding.default()

    if isinstance(rm, llvm.Register):
        encoding.modrm_mod = 0b11
        encoding.modrm_rm = rm.low3bits()
        encoding.rex_b = 0b0001 if rm.high_bit() else 0b0000

    elif isinstance(rm, llvm.RelativeAddress):
        encoding.modrm_mod = 0b00
        encoding.modrm_rm = 0b101
        encoding.disp_width = 4
        encoding.disp_value = rm.disp.value

    else:
        has_base = rm.base.is_available()
        has_index = rm.scaler.index.is_available()
        is_rsp_r12 = has_base and rm.base.low3bits() == 0b100
        is_rbp_r13 = has_base and rm.base.low3bits() == 0b101

        # RSP cannot be used as index register
        if has_index and rm.scaler.index.id == 0b0100:
            raise UnreachableEncodingError()

        if not has_base or has_index or is_rsp_r12:
            encoding.modrm_mod = 0b00
            encoding.modrm_rm = 0b100

            if has_index:
                encoding.sib_index = rm.scaler.index.low3bits()
                encoding.sib_scale = [1, 2, 4, 8].index(int(rm.scaler.scale))
                encoding.rex_x = 0b0010 if rm.scaler.index.high_bit() else 0b0000
            else:
                encoding.sib_index = 0b100
                encoding.sib_scale = 0b00

            if has_base:
                encoding.sib_base = rm.base.low3bits()
                encoding.rex_b = 0b0001 if rm.base.high_bit() else 0b0000
                encoding.disp_width = 0
            else:
                encoding.sib_base = 0b101
                encoding.disp_width = 4

        else:
            encoding.modrm_mod = 0b00
            encoding.modrm_rm = rm.base.low3bits()
            encoding.rex_b = 0b0001 if rm.base.high_bit() else 0b0000
            encoding.disp_width = 0

        if is_rbp_r13 and encoding.disp_width == 0:
            encoding.modrm_mod = 0b01
            encoding.disp_width = 1

        if encoding.disp_width < rm.disp.width // 8:
            if rm.disp.width == 8:
                encoding.modrm_mod = 0b01
                encoding.disp_width = 1
            else:
                encoding.modrm_mod = 0b10
                encoding.disp_width = 4

        encoding.disp_value = rm.disp.value

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
        bytecode.extend(
            modrm_rm.disp_value.to_bytes(
                modrm_rm.disp_width, byteorder="little", signed=True
            )
        )


def write_opcode(
    bytecode: bytearray,
    opcode_length: int,
    opcode_value: int,
    /,
    opcode_reg: Optional[OpCodeEncoding] = None,
) -> None:

    # append opcode register bits to opcode value if present
    if opcode_reg is not None:
        opcode_value |= opcode_reg.opcode_reg

    # opcode is blindly encoded as big-endian, because we human provide it this way
    bytecode.extend(opcode_value.to_bytes(opcode_length, byteorder="big", signed=False))


def write_immediate(
    bytecode: bytearray,
    imm: llvm.Immediate,
    /,
    condition: bool = True,
    signed: bool = False,
) -> None:
    if condition:
        bytecode.extend(
            imm.value.to_bytes(imm.width // 8, byteorder="little", signed=signed)
        )
