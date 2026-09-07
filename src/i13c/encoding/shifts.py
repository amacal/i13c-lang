from i13c.encoding import kind
from i13c.encoding.core import RelocationInfo
from i13c.encoding.kind import AddressInfo, RegisterInfo, ImmediateInfo
from i13c.semantic.typing.analyses.llvm import (
    RCL,
    RCR,
    ROL,
    ROR,
    SAL,
    SAR,
    SHL,
    SHR,
    Group2Instruction,
    Immediate,
    Register,
    Address,
    Relocation,
)


def encode_rcl(instruction: RCL, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group(0x02, instruction, bytecode)


def encode_rcr(instruction: RCR, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group(0x03, instruction, bytecode)


def encode_rol(instruction: ROL, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group(0x00, instruction, bytecode)


def encode_ror(instruction: ROR, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group(0x01, instruction, bytecode)


def encode_sal(instruction: SAL, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group(0x04, instruction, bytecode)


def encode_sar(instruction: SAR, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group(0x07, instruction, bytecode)


def encode_shl(instruction: SHL, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group(0x04, instruction, bytecode)


def encode_shr(instruction: SHR, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group(0x05, instruction, bytecode)


def encode_group(
    ext: int,
    instruction: Group2Instruction,
    bytecode: bytearray,
) -> RelocationInfo | None:
    # sanity check
    assert len(instruction.operands) == 2

    # extract operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # assume no immediate, nor relocation for now
    relocation: RelocationInfo | None = None
    immediate: Immediate | None = None
    is_8bit: bool = False

    # only r/m can be 8-bit
    is_8bit |= isinstance(dst, Register) and RegisterInfo.is_8bit(dst)
    is_8bit |= isinstance(dst, Address) and AddressInfo.is_8bit(dst)

    # the shift stored in CL has to be handled explicitly
    if isinstance(src, Register):
        opcode = 0xD2 if is_8bit else 0xD3

    # the same about the immediate value of 1, which has a dedicated encoding
    elif ImmediateInfo.is_one(src):
        opcode = 0xD0 if is_8bit else 0xD1

    # otherwise fallback to the a bit longer imm8 encoding
    else:
        opcode = 0xC0 if is_8bit else 0xC1
        immediate = src

    # compute ModRM fields
    modrm_reg = kind.encode_modrm_reg(ext)
    modrm_rm = kind.encode_modrm_rm(dst)

    # derive prefixes and rex
    prefixes = kind.encode_prefixes(dst)
    rex = kind.encode_rex(dst, modrm_reg=modrm_reg, modrm_rm=modrm_rm)

    # encode instruction
    kind.write_prefixes(bytecode, prefixes)
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 1, opcode)
    kind.write_modrm(bytecode, modrm_reg, modrm_rm)

    # if the dst operand is not an address with a relocation displacement
    if isinstance(dst, Address) and isinstance(dst.disp, Relocation):
        relocation = RelocationInfo(
            target=dst.disp.block,
            offset=len(bytecode) - 4,
            width=4,
        )

    # encode optional immediate
    kind.write_immediate(bytecode, immediate, condition=immediate is not None)

    # relocate if needed
    return relocation
