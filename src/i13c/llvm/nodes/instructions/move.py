from typing import Dict, Protocol, Tuple

from i13c.core.generator import Generator
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.core import (
    ComputedAddress,
    Displacement,
    Immediate,
    Register,
    Scaler,
)
from i13c.llvm.typing.instructions.move import (
    MovOffImm,
    MovOffReg,
    MovRegImm,
    MovRegOff,
    MovRegReg,
)
from i13c.llvm.typing.registers import IR_REGISTER_FORWARD_64
from i13c.semantic.typing.resolutions.addresses import AddressAcceptance
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
        MovRegImm(dst=dst, imm=imm),
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
        MovRegReg(dst=dst, src=src),
    )


def lower_address_immediate(
    generator: Generator,
    destination: AddressAcceptance,
    source: ImmediateAcceptance,
) -> InstructionEntry:

    dst = Register.parse64(destination.base.name.decode())
    imm = Immediate(data=source.value.data, width=source.value.width)
    off = destination.offset if destination.offset is not None else bytes([0x00])

    return (
        InstructionId(value=generator.next()),
        MovOffImm(
            dst=ComputedAddress(
                base=dst,
                disp=Displacement.auto(off),
                scaler=Scaler.none(),
                width=64,
            ),
            imm=imm,
        ),
    )


def lower_address_register(
    generator: Generator,
    destination: AddressAcceptance,
    source: RegisterAcceptance,
) -> InstructionEntry:

    dst = Register.parse64(destination.base.name.decode())
    src = IR_REGISTER_FORWARD_64[source.name]
    off = destination.offset if destination.offset is not None else bytes([0x00])

    return (
        InstructionId(value=generator.next()),
        MovOffReg(
            dst=ComputedAddress(
                base=dst,
                disp=Displacement.auto(off),
                scaler=Scaler.none(),
                width=64,
            ),
            src=src,
        ),
    )


def lower_register_address(
    generator: Generator,
    destination: RegisterAcceptance,
    source: AddressAcceptance,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD_64[destination.name]
    src = Register.parse64(source.base.name.decode())
    off = source.offset if source.offset is not None else bytes([0x00])

    return (
        InstructionId(value=generator.next()),
        MovRegOff(
            dst=dst,
            src=ComputedAddress(
                base=src,
                disp=Displacement.auto(off),
                scaler=Scaler.none(),
                width=64,
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
    ("reg64", "imm32"): lower_register_immediate,
    ("reg64", "reg64"): lower_register_register,
    ("addr", "imm32"): lower_address_immediate,
    ("addr", "reg64"): lower_address_register,
    ("reg64", "addr"): lower_register_address,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_mov(
    generator: Generator,
    instruction: InstructionAcceptance,
) -> InstructionEntry:

    # find operands
    dst = instruction.operands[0]
    src = instruction.operands[1]

    # find handler and call it
    handler = DISPATCH_TABLE[(dst.symbol, src.symbol)]
    return handler(generator, dst.target, src.target)
