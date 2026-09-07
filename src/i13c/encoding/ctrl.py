from i13c.encoding import kind
from i13c.encoding.core import RelocationInfo
from i13c.encoding.kind import DisplacementInfo

from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.analyses.asmlets import AsmletId
from i13c.semantic.typing.analyses.llvm import (
    CALL,
    JMP,
    LOOP,
    LOOPE,
    LOOPNE,
    NOP,
    RET,
    SYSCALL,
    Relocation,
    Address,
)


def encode_syscall(instruction: SYSCALL, bytecode: bytearray) -> None:
    # encode instruction
    kind.write_opcode(bytecode, 2, 0x0F05)


def encode_ret(instruction: RET, bytecode: bytearray) -> None:
    # encode instruction
    kind.write_opcode(bytecode, 1, 0xC3)


def encode_call(instruction: CALL, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group_call(0xE8, 0x02, instruction, bytecode)


def encode_jmp(instruction: JMP, bytecode: bytearray) -> RelocationInfo | None:
    return encode_group_call(0xE9, 0x04, instruction, bytecode)


def encode_group_call(
    opcode: int,
    ext: int,
    instruction: CALL | JMP,
    bytecode: bytearray,
) -> RelocationInfo | None:
    # sanity check
    assert len(instruction.operands) == 1

    # assme no rm, nor relocation for now
    block: int = 0
    reg: kind.ModRegEncoding | None = None
    rm: kind.ModRMEncoding | None = None
    rex: kind.RexEncoding | None = None
    relocation: RelocationInfo | None = None
    relocated: FunctionId | AsmletId | int | None = None

    # extract operands
    target = instruction.operands[0]

    # relocation enforces rel32 with a block inside
    if isinstance(target, Relocation):
        block = target.block
        relocated = target.block

    # function or asmlet enforces rel32 with a block inside
    elif isinstance(target, (FunctionId, AsmletId)):
        block = target.value
        relocated = target

    # otherwise address or register
    else:
        opcode = 0xFF

        reg = kind.encode_modrm_reg(ext)
        rm = kind.encode_modrm_rm(target)
        rex = kind.encode_rex(None, modrm_reg=reg, modrm_rm=rm)

    # encode as ModR/M if applicable
    if rm is not None and reg is not None and rex is not None:
        kind.write_rex(bytecode, rex)
        kind.write_opcode(bytecode, 1, opcode)
        kind.write_modrm(bytecode, reg, rm)

        # check if the r/m operand has a relocation displacement
        if isinstance(target, Address) and isinstance(target.disp, Relocation):
            relocation = RelocationInfo(
                target=target.disp.block,
                offset=len(bytecode) - 4,
                width=4,
            )

    # encode as fixed displacement
    else:
        assert relocated is not None

        kind.write_opcode(bytecode, 1, opcode)
        bytecode.extend(DisplacementInfo.fixed(block, 32))

        # returned relocation info
        relocation = RelocationInfo(
            target=relocated,
            offset=len(bytecode) - 4,
            width=4,
        )

    return relocation


def encode_loop(instruction: LOOP, bytecode: bytearray) -> RelocationInfo:
    return encode_group_loop(0xE2, instruction, bytecode)


def encode_loope(instruction: LOOPE, bytecode: bytearray) -> RelocationInfo:
    return encode_group_loop(0xE1, instruction, bytecode)


def encode_loopne(instruction: LOOPNE, bytecode: bytearray) -> RelocationInfo:
    return encode_group_loop(0xE0, instruction, bytecode)


def encode_group_loop(
    opcode: int, instruction: LOOP | LOOPE | LOOPNE, bytecode: bytearray
) -> RelocationInfo:
    # sanity check
    assert len(instruction.operands) == 1

    # extract operands
    target = instruction.operands[0]

    # LOOP rel8
    kind.write_opcode(bytecode, 1, opcode)

    # Reserve signed rel8 displacement.
    bytecode.extend(DisplacementInfo.fixed(target.block, 8))

    return RelocationInfo(
        target=target.block,
        offset=len(bytecode) - 1,
        width=1,
    )


def encode_nop(instruction: NOP, bytecode: bytearray) -> None:
    # encode instruction
    kind.write_opcode(bytecode, 1, 0x90)
