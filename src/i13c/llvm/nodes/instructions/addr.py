from typing import Dict, Protocol, Tuple

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.addr import LeaInstruction
from i13c.llvm.typing.instructions.core import ComputedAddress, Displacement
from i13c.llvm.typing.instructions.core import Register as Reg
from i13c.llvm.typing.instructions.core import Scaler
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import (
    Address,
    Operand,
    OperandId,
    OperandSymbol,
    OperandTarget,
    Register,
)


def lower_reg32_addr(
    generator: Generator,
    destination: Register,
    source: Address,
) -> InstructionEntry:
    return (
        InstructionId(value=generator.next()),
        LeaInstruction(
            kind="op+mod+reg",
            dst=Reg.parse32(destination.name.decode()),
            src=ComputedAddress(
                base=Reg.parse64(source.base.name.decode()),
                disp=Displacement.auto(source.offset),
                scaler=Scaler.none(),
            ),
        ),
    )


def lower_reg64_addr(
    generator: Generator,
    destination: Register,
    source: Address,
) -> InstructionEntry:
    return (
        InstructionId(value=generator.next()),
        LeaInstruction(
            kind="op+mod+reg",
            dst=Reg.parse64(destination.name.decode()),
            src=ComputedAddress(
                base=Reg.parse64(source.base.name.decode()),
                disp=Displacement.auto(source.offset),
                scaler=Scaler.none(),
            ),
        ),
    )


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        destination: OperandTarget,
        source: OperandTarget,
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[Tuple[OperandSymbol, OperandSymbol], InstructionHandler] = {
    (b"reg32", b"addr"): lower_reg32_addr,
    (b"reg64", b"addr"): lower_reg64_addr,
}  # pyright: ignore[reportAssignmentType]


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
    handler = DISPATCH_TABLE[(dst.target.symbol(), src.target.symbol())]
    return handler(generator, dst.target, src.target)
