from typing import List

from i13c import ast, diag, err
from i13c.sem.graph import Graph


def validate_immediate_out_of_range(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for instruction in graph.nodes.instructions.values():
        for operand in instruction.operands:
            if isinstance(operand, ast.Immediate):
                if not (0 <= operand.value <= 0xFFFFFFFFFFFFFFFF):
                    diagnostics.append(
                        err.report_e3001_immediate_out_of_range(
                            instruction.ref,
                            operand.value,
                        )
                    )

    return diagnostics
