from typing import Dict, Protocol, Tuple

from i13c.core.generator import Generator
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.bits import BSWAP
from i13c.llvm.typing.instructions.core import Register
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
from i13c.semantic.typing.resolutions.operands import OperandSymbol, OperandTarget
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance


def lower_reg32(
    generator: Generator,
    target: RegisterAcceptance,
) -> InstructionEntry:

    return (
        InstructionId(value=generator.next()),
        BSWAP(dst=Register.parse32(target.name.decode())),
    )


def lower_reg64(
    generator: Generator,
    target: RegisterAcceptance,
) -> InstructionEntry:

    return (
        InstructionId(value=generator.next()),
        BSWAP(dst=Register.parse64(target.name.decode())),
    )


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        target: OperandTarget,
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[Tuple[OperandSymbol], InstructionHandler] = {
    ("reg32",): lower_reg32,
    ("reg64",): lower_reg64,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_bswap(
    generator: Generator,
    instruction: InstructionAcceptance,
) -> InstructionEntry:

    # find operands
    dst = instruction.operands[0]

    # find handler and call it
    handler = DISPATCH_TABLE[(dst.symbol,)]
    return handler(generator, dst.target)
