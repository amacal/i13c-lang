from typing import Dict, Protocol, Tuple, Type

from i13c.core.generator import Generator
from i13c.core.mapping import OneToOne
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.core import (
    ComputedAddress,
    Displacement,
)
from i13c.llvm.typing.instructions.core import Immediate as Imm
from i13c.llvm.typing.instructions.core import Register as Reg
from i13c.llvm.typing.instructions.core import (
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
from i13c.semantic.typing.entities.instructions import (
    Instruction as SemanticInstruction,
)
from i13c.semantic.typing.entities.operands import (
    Address,
    Immediate,
    Operand,
    OperandId,
    OperandTarget,
    Register,
)


def lower_register_immediate(
    generator: Generator,
    destination: Register,
    source: Immediate,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD_64[destination.name]
    imm = Imm(data=source.data, width=source.width)

    return (
        InstructionId(value=generator.next()),
        MovRegImm(dst=dst, imm=imm),
    )


def lower_register_register(
    generator: Generator,
    destination: Register,
    source: Register,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD_64[destination.name]
    src = IR_REGISTER_FORWARD_64[source.name]

    return (
        InstructionId(value=generator.next()),
        MovRegReg(dst=dst, src=src),
    )


def lower_address_immediate(
    generator: Generator,
    destination: Address,
    source: Immediate,
) -> InstructionEntry:

    dst = Reg.parse64(destination.base.name.decode())
    imm = Imm(data=source.data, width=source.width)
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
    destination: Address,
    source: Register,
) -> InstructionEntry:

    dst = Reg.parse64(destination.base.name.decode())
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
    destination: Register,
    source: Address,
) -> InstructionEntry:

    dst = IR_REGISTER_FORWARD_64[destination.name]
    src = Reg.parse64(source.base.name.decode())
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


DISPATCH_TABLE: Dict[
    Tuple[Type[OperandTarget], Type[OperandTarget]], InstructionHandler
] = {
    (Register, Immediate): lower_register_immediate,
    (Register, Register): lower_register_register,
    (Address, Immediate): lower_address_immediate,
    (Address, Register): lower_address_register,
    (Register, Address): lower_register_address,
}  # pyright: ignore[reportAssignmentType]


def lower_instruction_mov(
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
