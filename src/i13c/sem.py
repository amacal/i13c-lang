from typing import List, Tuple, Type
from dataclasses import dataclass
from i13c import ast, src


class UnknownInstruction(Exception):
    def __init__(self, ref: ast.Reference) -> None:
        self.ref = ref


class InvalidOperandTypes(Exception):
    def __init__(self, ref: ast.Reference, found: List[str]) -> None:
        self.ref = ref
        self.found = found


@dataclass(kw_only=True)
class InstructionSignature:
    variants: List[Tuple[Type, ...]]


INSTRUCTIONS_TABLE = {
    b"syscall": InstructionSignature(variants=[()]),
    b"mov": InstructionSignature(variants=[(ast.Register, ast.Immediate)]),
}


def validate(program: ast.Program) -> None:
    for instruction in program.instructions:
        validate_instruction(instruction)


def validate_instruction(instruction: ast.Instruction) -> None:
    matched = False
    signature = INSTRUCTIONS_TABLE.get(instruction.mnemonic.name)

    if signature is None:
        raise UnknownInstruction(instruction.ref)

    # early acceptance for instructions without operands
    if not instruction.operands and not signature.variants:
        return

    for variant in signature.variants:

        # check operand count
        if len(variant) != len(instruction.operands):
            continue

        # check each operand type
        for expected, operand in zip(variant, instruction.operands):
            if not isinstance(operand, expected):
                break

        else:
            matched = True
            break

    if not matched:
        raise InvalidOperandTypes(
            instruction.ref,
            found=[type(op).__name__ for op in instruction.operands],
        )
