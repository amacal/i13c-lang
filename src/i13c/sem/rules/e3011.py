from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_entrypoint_exists(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:

    if len(graph.entrypoints) > 0:
        return []

    return [err.report_e3011_missing_entrypoint_function()]
