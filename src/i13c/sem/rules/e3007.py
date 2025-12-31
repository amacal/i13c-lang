from typing import List, Optional, Union

from i13c import diag, err
from i13c.sem.function import Function, FunctionId
from i13c.sem.model import SemanticGraph
from i13c.sem.snippet import Snippet, SnippetId


def validate_called_symbol_resolved(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for cid, resolution in graph.indices.resolution_by_callsite.items():
        if not resolution.accepted:

            # not resolved but some candidates were rejected
            if resolution.rejected:
                variants: List[str] = []

                for rejection in resolution.rejected:
                    reason = rejection.reason.decode()
                    callable = rejection.callable.target
                    target: Optional[Union[Function, Snippet]] = None

                    if rejection.callable.kind == b"function":
                        assert isinstance(callable, FunctionId)
                        target = graph.basic.functions.get(callable)

                    if rejection.callable.kind == b"snippet":
                        assert isinstance(callable, SnippetId)
                        target = graph.basic.snippets.get(callable)

                    assert target, "resolved callable must exist"
                    variants.append(f"{reason}: {target.signature()}")

                diagnostics.append(
                    err.report_e3007_no_matching_overload(
                        graph.basic.callsites.get(cid).ref,
                        graph.basic.callsites.get(cid).callee.name,
                        variants,
                    )
                )

    return diagnostics
