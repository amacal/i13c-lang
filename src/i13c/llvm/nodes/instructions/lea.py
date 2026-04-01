from typing import Dict, Protocol, Tuple, Type

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.instructions import (
    InstructionEntry,
    InstructionId,
    LeaRegOff,
)
from i13c.llvm.typing.registers import IR_REGISTER_FORWARD_64
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import (
    Address,
    Operand,
    OperandId,
    OperandTarget,
    Register,
)


def lower_register_address(
    generator: Generator,
    destination: Register,
    source: Address,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD_64[destination.name]
    src = IR_REGISTER_FORWARD_64[source.base.name]
    off = source.offset.value if source.offset is not None else 0

    return (
        InstructionId(value=generator.next()),
        LeaRegOff(dst=dst, off=off, src=src),
    )


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        destination: OperandTarget,
        source: OperandTarget,
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[
    Tuple[Type[OperandTarget], Type[OperandTarget]], InstructionHandler
] = {
    (
        Register,
        Address,
    ): lower_register_address,  # pyright: ignore[reportAssignmentType]
}


def lower_instruction_lea(
    generator: Generator,
    operands: OneToOne[OperandId, Operand],
    instruction: SemanticInstruction,
    rewritten: Dict[OperandId, Operand],
) -> InstructionEntry:

    # first try out rewritten operands
    dst = rewritten.get(instruction.operands[0])
    src = rewritten.get(instruction.operands[1])

    # fallback to original operands if not rewritten
    dst = dst or operands.get(instruction.operands[0])
    src = src or operands.get(instruction.operands[1])

    # find handler and call it
    handler = DISPATCH_TABLE[(type(dst.target), type(src.target))]
    return handler(generator, dst.target, src.target)
