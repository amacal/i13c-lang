from i13c.encoding import kind
from i13c.semantic.typing.analyses.llvm import BSWAP


def encode_bswap(instruction: BSWAP, bytecode: bytearray) -> None:
    # sanity check
    assert len(instruction.operands) == 1

    # extract operands
    target = instruction.operands[0]

    # derive opcode and rex
    opcode_reg = kind.encode_opcode_reg(target)
    rex = kind.encode_rex(target, opcode_reg=opcode_reg)

    # encode instruction
    kind.write_rex(bytecode, rex)
    kind.write_opcode(bytecode, 2, 0x0FC8, opcode_reg=opcode_reg)
