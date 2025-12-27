from typing import List, Set

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_duplicated_parameter_names(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for snippet in graph.snippets.values():
        seen: Set[bytes] = set()

        for slot in snippet.slots:
            if slot.name.name in seen:
                diagnostics.append(
                    err.report_e3004_duplicated_parameter_names(
                        snippet.ref, slot.name.name
                    )
                )
            else:
                seen.add(slot.name.name)

    for function in graph.functions.values():
        seen: Set[bytes] = set()

        for parameter in function.parameters:
            if parameter.name.name in seen:
                diagnostics.append(
                    err.report_e3004_duplicated_parameter_names(
                        function.ref, parameter.name.name
                    )
                )
            else:
                seen.add(parameter.name.name)

    return diagnostics
