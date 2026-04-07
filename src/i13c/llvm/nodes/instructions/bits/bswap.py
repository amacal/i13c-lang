from typing import Dict, Protocol, Tuple

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.bits import BSWAP
from i13c.llvm.typing.instructions.core import Register as Reg
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import (
    Operand,
    OperandId,
    OperandSymbol,
    OperandTarget,
    Register,
)


def lower_reg32(
    generator: Generator,
    target: Register,
) -> InstructionEntry:

    return (
        InstructionId(value=generator.next()),
        BSWAP(dst=Reg.parse32(target.name.decode())),
    )


def lower_reg64(
    generator: Generator,
    target: Register,
) -> InstructionEntry:

    return (
        InstructionId(value=generator.next()),
        BSWAP(dst=Reg.parse64(target.name.decode())),
    )


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        target: OperandTarget,
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[Tuple[OperandSymbol], InstructionHandler] = {
    (b"reg32",): lower_reg32,
    (b"reg64",): lower_reg64,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_bswap(
    generator: Generator,
    operands: OneToOne[OperandId, Operand],
    instruction: SemanticInstruction,
    rewritten: Dict[OperandId, Operand],
) -> InstructionEntry:

    # first try out rewritten operand
    dst = rewritten.get(instruction.operands[0])

    # fallback to original operand if not rewritten
    dst = dst or operands.get(instruction.operands[0])

    # find handler and call it
    handler = DISPATCH_TABLE[(dst.target.symbol(),)]
    return handler(generator, dst.target)
