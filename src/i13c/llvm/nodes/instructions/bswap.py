from typing import Dict

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.instructions import (
    ByteSwap,
    InstructionEntry,
    InstructionId,
)
from i13c.llvm.typing.registers import IR_REGISTER_FORWARD
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import Operand, OperandId, Register


def lower_instruction_bswap(
    generator: Generator,
    operands: OneToOne[OperandId, Operand],
    instruction: SemanticInstruction,
    rewritten: Dict[OperandId, Operand],
) -> InstructionEntry:

    # first try out rewritten operands
    dst = rewritten.get(instruction.operands[0])

    # fallback to original operands if not rewritten
    dst = dst or operands.get(instruction.operands[0])

    # make sure the operand is a register
    assert isinstance(dst.target, Register)

    target = IR_REGISTER_FORWARD[dst.target.name]
    return (InstructionId(value=generator.next()), ByteSwap(target=target))
