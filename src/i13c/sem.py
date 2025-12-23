from dataclasses import dataclass
from typing import List, Set, Tuple, Type, Union

from i13c import ast, diag, err, src


class UnknownInstruction(Exception):
    def __init__(self, ref: src.Span) -> None:
        self.ref = ref


class InvalidOperandTypes(Exception):
    def __init__(self, ref: src.Span, found: List[str]) -> None:
        self.ref = ref
        self.found = found


class ImmediateOutOfRange(Exception):
    def __init__(self, ref: src.Span, value: int) -> None:
        self.ref = ref
        self.value = value


AllowedVariants = Union[Type[ast.Register], Type[ast.Immediate]]


@dataclass(kw_only=True)
class InstructionSignature:
    variants: List[Tuple[AllowedVariants, ...]]


INSTRUCTIONS_TABLE = {
    b"syscall": InstructionSignature(variants=[()]),
    b"mov": InstructionSignature(variants=[(ast.Register, ast.Immediate)]),
}


def validate(program: ast.Program) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []
    function_names: Set[bytes] = set()

    for function in program.functions:
        if function.name not in function_names:
            function_names.add(function.name)
            validate_function(diagnostics, function)

        else:
            diagnostics.append(
                err.report_e3006_duplicated_function_names(function.ref, function.name)
            )

    return diagnostics


def validate_function(
    diagnostics: List[diag.Diagnostic],
    function: Union[ast.AsmFunction, ast.RegFunction],
) -> None:
    if isinstance(function, ast.AsmFunction):
        validate_asm_function(diagnostics, function)

    else:
        validate_reg_function(diagnostics, function)


def validate_reg_function(
    diagnostics: List[diag.Diagnostic], function: ast.RegFunction
) -> None:

    validate_reg_parameters(diagnostics, function)

    for statement in function.statements:
        validate_statement(diagnostics, statement)


def validate_asm_function(
    diagnostics: List[diag.Diagnostic], function: ast.AsmFunction
) -> None:

    validate_asm_parameters(diagnostics, function)
    validate_asm_clobbers(diagnostics, function)

    for instruction in function.instructions:
        validate_instruction(diagnostics, instruction)


def validate_reg_parameters(
    diagnostics: List[diag.Diagnostic], function: ast.RegFunction
) -> None:
    names: Set[bytes] = set()

    for parameter in function.parameters:
        if parameter.name in names:
            diagnostics.append(
                err.report_e3004_duplicated_parameter_names(
                    function.ref, parameter.name
                )
            )
        else:
            names.add(parameter.name)


def validate_asm_parameters(
    diagnostics: List[diag.Diagnostic], function: ast.AsmFunction
) -> None:
    names: Set[bytes] = set()
    bindings: Set[bytes] = set()

    for parameter in function.parameters:
        if parameter.name in names:
            diagnostics.append(
                err.report_e3004_duplicated_parameter_names(
                    function.ref, parameter.name
                )
            )
        else:
            names.add(parameter.name)

        if parameter.bind.name in bindings:
            diagnostics.append(
                err.report_e3003_duplicated_bindings(function.ref, parameter.bind.name)
            )
        else:
            bindings.add(parameter.bind.name)


def validate_asm_clobbers(
    diagnostics: List[diag.Diagnostic], function: ast.AsmFunction
) -> None:
    seen: Set[bytes] = set()

    for clobber in function.clobbers:
        if clobber.name in seen:
            diagnostics.append(
                err.report_e3005_duplicated_clobbers(function.ref, clobber.name)
            )
        else:
            seen.add(clobber.name)


def validate_statement(
    diagnostics: List[diag.Diagnostic], statement: ast.CallStatement
) -> None:

    for argument in statement.arguments:
        if not (0 <= argument.value <= 0xFFFFFFFFFFFFFFFF):
            diagnostics.append(
                err.report_e3007_integer_literal_out_of_range(
                    statement.ref, argument.value
                )
            )


def validate_instruction(
    diagnostics: List[diag.Diagnostic], instruction: ast.Instruction
) -> None:
    matched = False
    signature = INSTRUCTIONS_TABLE.get(instruction.mnemonic.name)

    # missing instruction mnemonic
    if signature is None:
        diagnostics.append(err.report_e3000_unknown_instruction(instruction.ref))
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
                            err.report_e3001_immediate_out_of_range(
                                instruction.ref, operand.value
                            )
                        )

            matched = True
            break

    if not matched:
        diagnostics.append(
            err.report_e3002_invalid_operand_types(
                instruction.ref,
                [type(operand).__name__ for operand in instruction.operands],
            )
        )
