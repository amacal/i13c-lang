from typing import List, Optional, Union

from i13c import diag, err
from i13c.core.dag import GraphNode
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId


def configure_e3007() -> GraphNode:
    return GraphNode(
        builder=validate_called_symbol_resolved,
        produces=("rules/e3007",),
        requires=frozenset({("graph", "semantic/graph")}),
    )


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
