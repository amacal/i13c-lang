from typing import Dict, Protocol

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.nodes.instructions import addr, bits, math, move
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.ctrl import SysCall
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import Operand, OperandId


def lower_instruction(
    generator: Generator,
    operands: OneToOne[OperandId, Operand],
    instruction: SemanticInstruction,
    rewritten: Dict[OperandId, Operand],
) -> InstructionEntry:

    if instruction.mnemonic.name in DISPATCH_TABLE:
        return DISPATCH_TABLE[instruction.mnemonic.name](
            generator, operands, instruction, rewritten
        )

    assert False, f"unsupported mnemonic: {instruction.mnemonic.name}"


def lower_instruction_syscall(
    generator: Generator,
    operands: OneToOne[OperandId, Operand],
    instruction: SemanticInstruction,
    rewritten: Dict[OperandId, Operand],
) -> InstructionEntry:

    # syscall has no operands, so we can ignore them
    return (InstructionId(value=generator.next()), SysCall())


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        operands: OneToOne[OperandId, Operand],
        instruction: SemanticInstruction,
        rewritten: Dict[OperandId, Operand],
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[bytes, InstructionHandler] = {
    b"add": math.lower_instruction_add,
    b"bswap": bits.lower_instruction_bswap,
    b"lea": addr.lower_instruction_lea,
    b"mov": move.lower_instruction_mov,
    b"shl": bits.lower_instruction_shl,
    b"syscall": lower_instruction_syscall,
}  # pyright: ignore[reportAssignmentType]
