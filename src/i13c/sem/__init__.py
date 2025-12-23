from typing import Callable, List, Union

from i13c import ast, diag, src, sym
from i13c.sem.rules import (e3000, e3001, e3002, e3003, e3004, e3005, e3006,
                            e3007)


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


RULES: List[Callable[[ast.Program], List[diag.Diagnostic]]] = [
    e3000.validate_assembly_mnemonic,
    e3001.validate_immediate_out_of_range,
    e3002.validate_assembly_operand_types,
    e3003.validate_duplicated_parameter_bindings,
    e3004.validate_duplicated_parameter_names,
    e3005.validate_duplicated_function_clobbers,
    e3006.validate_duplicated_function_names,
    e3007.validate_integer_literal_out_of_range,
]


def validate(program: ast.Program) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for rule in RULES:
        diagnostics.extend(rule(program))

    return diagnostics


def aggregate(program: ast.Program) -> sym.SymbolTable:
    entries: List[sym.SymbolTableEntry] = []

    for function in program.functions:
        entries.append(
            sym.SymbolTableEntry(
                ref=function.ref,
                name=function.name,
                target=into_symbol_target(function),
            )
        )

    return sym.SymbolTable(entries=entries)


def into_symbol_target(
    function: Union[ast.AsmFunction, ast.RegFunction],
) -> sym.SymbolFunction:
    parameters: List[sym.SigParameter] = []

    for parameter in function.parameters:
        parameters.append(
            sym.SigParameter(
                name=parameter.name,
                type=sym.SigType(name=parameter.type.name),
            )
        )

    return sym.SymbolFunction(parameters=parameters)
