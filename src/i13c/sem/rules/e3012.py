from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_entrypoint_never_returns(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:

    for fid, function in graph.functions.items():
        if function.identifier.name == b"main":
            # get the terminality info for this function
            terminality = graph.function_terminalities[fid]

            # complain if it is not noreturn
            if not terminality.noreturn:
                return [
                    err.report_e3012_non_terminal_entrypoint_function(
                        function.ref,
                    )
                ]

    return []
