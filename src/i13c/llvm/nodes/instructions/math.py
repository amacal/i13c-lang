from typing import Dict, Protocol, Tuple

from i13c.core.generator import Generator
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.core import Immediate
from i13c.llvm.typing.instructions.math import AddRegImm, AddRegReg
from i13c.llvm.typing.registers import IR_REGISTER_FORWARD_64
from i13c.semantic.typing.resolutions.immediates import ImmediateAcceptance
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
from i13c.semantic.typing.resolutions.operands import OperandSymbol, OperandTarget
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance


def lower_register_immediate(
    generator: Generator,
    destination: RegisterAcceptance,
    source: ImmediateAcceptance,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD_64[destination.name]
    imm = Immediate(data=source.value.data, width=source.value.width)

    return (
        InstructionId(value=generator.next()),
        AddRegImm(dst=dst, imm=imm),
    )


def lower_register_register(
    generator: Generator,
    destination: RegisterAcceptance,
    source: RegisterAcceptance,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD_64[destination.name]
    src = IR_REGISTER_FORWARD_64[source.name]

    return (
        InstructionId(value=generator.next()),
        AddRegReg(dst=dst, src=src),
    )


class InstructionHandler(Protocol):
    def __call__(
        self,
        generator: Generator,
        destination: OperandTarget,
        source: OperandTarget,
    ) -> InstructionEntry: ...


DISPATCH_TABLE: Dict[Tuple[OperandSymbol, OperandSymbol], InstructionHandler] = {
    ("reg64", "imm32"): lower_register_immediate,
    ("reg64", "reg64"): lower_register_register,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_add(
    generator: Generator,
    instruction: InstructionAcceptance,
) -> InstructionEntry:

    # find operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # find handler and call it
    handler = DISPATCH_TABLE[(dst.symbol, src.symbol)]
    return handler(generator, dst.target, src.target)
