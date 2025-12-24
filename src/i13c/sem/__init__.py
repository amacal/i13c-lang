from typing import Callable, List

from i13c import ast, diag
from i13c.sem.analysis import Analysis, build_analysis
from i13c.sem.graph import Graph, build_graph
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
    e3011,
    e3012,
)

RULES_1ST_PASS: List[Callable[[Graph], List[diag.Diagnostic]]] = [
    e3000.validate_assembly_mnemonic,
    e3001.validate_immediate_out_of_range,
    e3002.validate_assembly_operand_types,
    e3003.validate_duplicated_parameter_bindings,
    e3004.validate_duplicated_parameter_names,
    e3005.validate_duplicated_function_clobbers,
    e3006.validate_duplicated_function_names,
    e3007.validate_integer_literal_out_of_range,
]

RULES_2ND_PASS: List[Callable[[Graph, Analysis], List[diag.Diagnostic]]] = [
    e3008.validate_called_symbol_exists,
    e3009.validate_called_symbol_is_asm,
    e3010.validate_called_symbol_termination,
    e3011.validate_called_arguments_count,
    e3012.validate_called_arguments_types,
]


def validate(program: ast.Program) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []
    graph = build_graph(program)
    analysis = build_analysis(graph)

    diagnostics.extend(validate_1st_pass(graph))
    diagnostics.extend(validate_2nd_pass(graph, analysis))

    return diagnostics


def validate_1st_pass(graph: Graph) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for rule in RULES_1ST_PASS:
        diagnostics.extend(rule(graph))

    return diagnostics


def validate_2nd_pass(graph: Graph, analysis: Analysis) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for rule in RULES_2ND_PASS:
        diagnostics.extend(rule(graph, analysis))

    return diagnostics
