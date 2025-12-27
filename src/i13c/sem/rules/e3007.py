from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph
from i13c.sem.literal import Hex


def validate_integer_literal_out_of_range(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for literal in graph.literals.values():
        if literal.kind == b"hex":

            # satisfy type checker
            assert isinstance(literal.target, Hex)

            if literal.target.width is None:
                diagnostics.append(
                    err.report_e3007_integer_literal_out_of_range(
                        literal.ref,
                        literal.target.value,
                    )
                )

    return diagnostics
