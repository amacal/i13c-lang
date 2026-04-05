from dataclasses import dataclass
from typing import Union

from i13c.encoding.core import UnreachableEncodingError
from i13c.llvm.typing.instructions import core as llvm

RegisterOrAddress = Union[llvm.Register, llvm.ComputedAddress, llvm.RelativeAddress]


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


def encode_modrm_reg(reg: llvm.Register) -> ModRegEncoding:
    return ModRegEncoding(
        rex_w=0b1000 if reg.is_64bit() else 0b0000,
        rex_r=0b0100 if reg.high_bit() else 0b0000,
        modrm_reg=reg.low3bits(),
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


def write_rex(
    bytecode: bytearray,
    modrm_reg: ModRegEncoding,
    modrm_rm: ModRMEncoding,
    /,
    force: bool = False,
) -> None:
    prefix = 0x40
    bits = modrm_reg.rex_w | modrm_reg.rex_r | modrm_rm.rex_x | modrm_rm.rex_b

    if bits or force:
        bytecode.append(prefix | bits)


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
) -> None:

    # opcode is blindly encoded as big-endian, because we human provide it this way
    bytecode.extend(opcode_value.to_bytes(opcode_length, byteorder="big", signed=False))
