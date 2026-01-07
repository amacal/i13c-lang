from typing import Callable, List

from i13c import ast, diag
from i13c.sem.model import SemanticGraph
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
    e3010,
    e3011,
    e3012,
)

RULES: List[Callable[[SemanticGraph], List[diag.Diagnostic]]] = [
    e3000.validate_assembly_mnemonic,
    e3001.validate_type_ranges,
    e3002.validate_assembly_operand_types,
    e3003.validate_duplicated_slot_bindings,
    e3004.validate_duplicated_parameter_names,
    e3005.validate_duplicated_snippet_clobbers,
    e3006.validate_duplicated_function_names,
    e3007.validate_called_symbol_resolved,
    e3008.validate_called_symbol_exists,
    e3010.validate_called_symbol_terminality,
    e3011.validate_entrypoint_exists,
    e3012.validate_entrypoint_is_single,
]


def validate(model: SemanticGraph, program: ast.Program) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for rule in RULES:
        diagnostics.extend(rule(model))

    return diagnostics
