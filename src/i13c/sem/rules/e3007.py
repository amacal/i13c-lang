from typing import List

from i13c import diag, err
from i13c.sem.graph import Graph


def validate_integer_literal_out_of_range(
    graph: Graph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for literal in graph.nodes.literals.id_to_node.values():
        if not (0 <= literal.value <= 0xFFFFFFFFFFFFFFFF):
            diagnostics.append(
                err.report_e3007_integer_literal_out_of_range(
                    literal.ref,
                    literal.value,
                )
            )

    return diagnostics
