from typing import Callable, Dict, List, Union

from i13c import ast, diag, sym
from i13c.sem.rules import (
    e3000,
    e3001,
    e3002,
    e3003,
    e3004,
    e3005,
    e3006,
    e3007,
    e3008,
    e3009,
    e3010,
)

RULES_1ST_PASS: List[Callable[[ast.Program], List[diag.Diagnostic]]] = [
    e3000.validate_assembly_mnemonic,
    e3001.validate_immediate_out_of_range,
    e3002.validate_assembly_operand_types,
    e3003.validate_duplicated_parameter_bindings,
    e3004.validate_duplicated_parameter_names,
    e3005.validate_duplicated_function_clobbers,
    e3006.validate_duplicated_function_names,
    e3007.validate_integer_literal_out_of_range,
]

RULES_2ND_PASS: List[
    Callable[[ast.Program, sym.SymbolTable], List[diag.Diagnostic]]
] = [
    e3008.validate_called_symbol_exists,
    e3009.validate_called_symbol_is_asm,
    e3010.validate_called_symbol_termination,
]


def validate_1st_pass(program: ast.Program) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for rule in RULES_1ST_PASS:
        diagnostics.extend(rule(program))

    return diagnostics


def validate_2nd_pass(
    program: ast.Program, symbol_table: sym.SymbolTable
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for rule in RULES_2ND_PASS:
        diagnostics.extend(rule(program, symbol_table))

    return diagnostics


def aggregate(program: ast.Program) -> sym.SymbolTable:
    entries: Dict[bytes, sym.SymbolTableEntry] = {}

    for function in program.functions:
        entries[function.name] = sym.SymbolTableEntry(
            ref=function.ref,
            name=function.name,
            target=into_symbol_target(function),
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

    kind = (
        sym.FUNCTION_KIND_ASM
        if isinstance(function, ast.AsmFunction)
        else sym.FUNCTION_KIND_REG
    )

    return sym.SymbolFunction(
        kind=kind,
        terminal=function.terminal,
        parameters=parameters,
    )
