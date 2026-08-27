from i13c.encoding import kind
from i13c.encoding.core import RelocationInfo
from i13c.encoding.kind import DisplacementInfo
from i13c.semantic.typing.analyses.llvm import CALL, JMP, LOOP, NOP, RET, SYSCALL


def encode_syscall(instruction: SYSCALL, bytecode: bytearray) -> None:
    # encode instruction
    kind.write_opcode(bytecode, 2, 0x0F05)


def encode_ret(instruction: RET, bytecode: bytearray) -> None:
    # encode instruction
    kind.write_opcode(bytecode, 1, 0xC3)


def encode_call(instruction: CALL, bytecode: bytearray) -> RelocationInfo:
    # encode opcode
    kind.write_opcode(bytecode, 1, 0xE8)

    # reserve rel32 displacement
    bytecode.extend(DisplacementInfo.fixed(instruction.target.value, 32))

    # return relocation info
    return RelocationInfo(
        target=instruction.target,
        offset=len(bytecode) - 4,
        width=4,
    )


def encode_jmp(instruction: JMP, bytecode: bytearray) -> RelocationInfo:
    # sanity check
    assert len(instruction.operands) == 1

    # extract operands
    target = instruction.operands[0]

    # encode opcode
    kind.write_opcode(bytecode, 1, 0xE9)

    # reserve rel32 displacement
    bytecode.extend(DisplacementInfo.fixed(target.block, 32))

    # return relocation info
    return RelocationInfo(
        target=target.block,
        offset=len(bytecode) - 4,
        width=4,
    )


def encode_loop(instruction: LOOP, bytecode: bytearray) -> RelocationInfo:
    # sanity check
    assert len(instruction.operands) == 1

    # extract operands
    target = instruction.operands[0]

    # LOOP rel8
    kind.write_opcode(bytecode, 1, 0xE2)

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
