from dataclasses import dataclass
from typing import List, Set, Tuple, Type

from i13c import ast, diag


class UnknownInstruction(Exception):
    def __init__(self, ref: ast.Span) -> None:
        self.ref = ref


class InvalidOperandTypes(Exception):
    def __init__(self, ref: ast.Span, found: List[str]) -> None:
        self.ref = ref
        self.found = found


class ImmediateOutOfRange(Exception):
    def __init__(self, ref: ast.Span, value: int) -> None:
        self.ref = ref
        self.value = value


@dataclass(kw_only=True)
class InstructionSignature:
    variants: List[Tuple[Type, ...]]


INSTRUCTIONS_TABLE = {
    b"syscall": InstructionSignature(variants=[()]),
    b"mov": InstructionSignature(variants=[(ast.Register, ast.Immediate)]),
}


def validate(program: ast.Program) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for function in program.functions:
        validate_function(diagnostics, function)

    return diagnostics


def validate_function(
    diagnostics: List[diag.Diagnostic], function: ast.Function
) -> None:

    validate_parameters(diagnostics, function)
    validate_clobbers(diagnostics, function)

    for instruction in function.instructions:
        validate_instruction(diagnostics, instruction)


def validate_parameters(
    diagnostics: List[diag.Diagnostic], function: ast.Function
) -> None:
    names: Set[bytes] = set()
    bindings: Set[bytes] = set()

    for parameter in function.parameters:
        if parameter.name in names:
            diagnostics.append(
                report_duplicated_parameter_names(
                    function.instructions[0].ref, parameter.name
                )
            )
        else:
            names.add(parameter.name)

        if parameter.bind.name in bindings:
            diagnostics.append(
                report_duplicated_bindings(function.ref, parameter.bind.name)
            )
        else:
            bindings.add(parameter.bind.name)


def validate_clobbers(
    diagnostics: List[diag.Diagnostic], function: ast.Function
) -> None:
    seen: Set[bytes] = set()

    for clobber in function.clobbers:
        if clobber.name in seen:
            diagnostics.append(report_duplicated_clobbers(function.ref, clobber.name))
        else:
            seen.add(clobber.name)


def validate_instruction(
    diagnostics: List[diag.Diagnostic], instruction: ast.Instruction
) -> None:
    matched = False
    signature = INSTRUCTIONS_TABLE.get(instruction.mnemonic.name)

    # missing instruction mnemonic
    if signature is None:
        diagnostics.append(report_unknown_instruction(instruction.ref))
        return

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
            for operand in instruction.operands:
                if isinstance(operand, ast.Immediate):
                    if not (0 <= operand.value <= 0xFFFFFFFFFFFFFFFF):
                        diagnostics.append(
                            report_immediate_out_of_range(
                                instruction.ref, operand.value
                            )
                        )

            matched = True
            break

    if not matched:
        diagnostics.append(
            report_invalid_operand_types(
                instruction.ref,
                [type(operand).__name__ for operand in instruction.operands],
            )
        )


def report_unknown_instruction(ref: ast.Span) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=ref.offset,
        code="V001",
        message=f"Unknown instruction mnemonic at offset {ref.offset}",
    )


def report_immediate_out_of_range(ref: ast.Span, value: int) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=ref.offset,
        code="V002",
        message=f"Immediate value {value} out of range at offset {ref.offset}",
    )


def report_invalid_operand_types(ref: ast.Span, found: List[str]) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=ref.offset,
        code="V003",
        message=f"Invalid operand types ({', '.join(found)}) at offset {ref.offset}",
    )


def report_duplicated_bindings(ref: ast.Span, found: bytes) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=ref.offset,
        code="V004",
        message=f"Duplicated parameter bindings for ({found.decode('utf-8')}) at offset {ref.offset}",
    )


def report_duplicated_parameter_names(ref: ast.Span, found: bytes) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=ref.offset,
        code="V005",
        message=f"Duplicated parameter names for ({found.decode('utf-8')}) at offset {ref.offset}",
    )


def report_duplicated_clobbers(ref: ast.Span, found: bytes) -> diag.Diagnostic:
    return diag.Diagnostic(
        offset=ref.offset,
        code="V006",
        message=f"Duplicated clobber registers for ({found.decode('utf-8')}) at offset {ref.offset}",
    )
