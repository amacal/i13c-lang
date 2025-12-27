from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_entrypoint_exists(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:

    # check for a function named "main"
    for function in graph.functions.values():
        if function.identifier.name == b"main":
            return []

    return [err.report_e3011_missing_entrypoint_function()]
