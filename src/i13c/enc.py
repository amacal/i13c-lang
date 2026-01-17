from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol, Type, Union

from i13c import ir


def encode(instructions: List[ir.InstructionFlow]) -> bytes:
    bytecode = bytearray()
    labels: Dict[int, Label] = {}
    relocations: List[Relocation] = []

    for instruction in instructions:
        if result := DISPATCH_TABLE[type(instruction)](instruction, bytecode):
            if isinstance(result, Label):
                labels[result.target] = result
            else:
                relocations.append(result)

    for relocation in relocations:
        target = labels[relocation.target].offset - (relocation.offset + 4)
        low, high = relocation.offset, relocation.offset + 4

        bytecode[low:high] = target.to_bytes(4, byteorder="little", signed=True)

    return bytes(bytecode)


def encode_mov_reg_imm(
    instruction: ir.MovRegImm, bytecode: bytearray
) -> Optional[Union[Label, Relocation]]:
    # REX.W + B8+rd io
    rex = 0x40 | 0x08 | (0x01 if instruction.dst >= 8 else 0x00)
    opcode = 0xB8 | (instruction.dst & 0x07)
    imm = instruction.imm.to_bytes(8, byteorder="little", signed=False)

    bytecode.extend([rex, opcode, *imm])


def encode_shl_reg_imm(
    instruction: ir.ShlRegImm, bytecode: bytearray
) -> Optional[Union[Label, Relocation]]:
    # REX.W + C1 /4 ib
    rex = 0x40 | 0x08 | (0x01 if instruction.dst >= 8 else 0x00)
    opcode = 0xC1
    modrm = 0xE0 | (4 << 3) | (instruction.dst & 0x07)
    imm = instruction.imm.to_bytes(1, byteorder="little", signed=False)

    bytecode.extend([rex, opcode, modrm, *imm])


def encode_syscall(
    instruction: ir.SysCall, bytecode: bytearray
) -> Optional[Union[Label, Relocation]]:
    bytecode.extend([0x0F, 0x05])


def encode_return(
    instruction: ir.Return, bytecode: bytearray
) -> Optional[Union[Label, Relocation]]:
    bytecode.extend([0xC3])


def encode_label(
    instruction: ir.Label, bytecode: bytearray
) -> Optional[Union[Label, Relocation]]:
    return Label(target=instruction.id, offset=len(bytecode))


def encode_call(
    instruction: ir.Call, bytecode: bytearray
) -> Optional[Union[Label, Relocation]]:
    bytecode.extend([0xE8, 0x00, 0x00, 0x00, 0x00])
    return Relocation(target=instruction.target.value, offset=len(bytecode) - 4)


@dataclass(kw_only=True)
class Label:
    target: int
    offset: int


@dataclass(kw_only=True)
class Relocation:
    target: int
    offset: int


class Encoder(Protocol):
    def __call__(
        self, instruction: ir.InstructionFlow, out: bytearray
    ) -> Optional[Union[Label, Relocation]]: ...


DISPATCH_TABLE: Dict[Type[ir.InstructionFlow], Encoder] = {
    ir.MovRegImm: encode_mov_reg_imm,
    ir.ShlRegImm: encode_shl_reg_imm,
    ir.SysCall: encode_syscall,
    ir.Return: encode_return,
    ir.Label: encode_label,
    ir.Call: encode_call,
}  # pyright: ignore[reportAssignmentType]
