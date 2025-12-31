from typing import List

from i13c import diag, err
from i13c.sem.model import SemanticGraph


def validate_entrypoint_is_single(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:

    if graph.live.entrypoints.size() <= 1:
        return []

    return [err.report_e3012_multiple_entrypoint_functions()]
