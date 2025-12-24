from typing import List

from i13c import diag, err
from i13c.sem import rel


def validate_integer_literal_out_of_range(
    relationships: rel.Relationships,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for literal in relationships.nodes.literals.id_to_node.values():
        if not (0 <= literal.value <= 0xFFFFFFFFFFFFFFFF):
            diagnostics.append(
                err.report_e3007_integer_literal_out_of_range(
                    literal.ref,
                    literal.value,
                )
            )

    return diagnostics
