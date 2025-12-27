from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_called_symbol_termination(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for fid, terminality in graph.function_terminalities.items():
        # we need to compare against the function definition
        function = graph.functions[fid]

        # if the terminality expectations do not match, report an error
        if function.noreturn != terminality.noreturn:
                diagnostics.append(
                    err.report_e3010_callee_is_non_terminal(
                        function.ref,
                        function.identifier.name,
                    )
                )

    return diagnostics
