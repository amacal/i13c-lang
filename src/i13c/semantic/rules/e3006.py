from typing import Iterable, List, Protocol, Set

from i13c import diag, err
from i13c.core.dag import GraphNode
from i13c.semantic.core import Identifier
from i13c.semantic.model import SemanticGraph
from i13c.src import Span


def configure_e3006() -> GraphNode:
    return GraphNode(
        builder=validate_duplicated_function_names,
        produces=("rules/e3006",),
        requires=frozenset({("graph", "semantic/graph")}),
    )


class Callable(Protocol):
    ref: Span
    identifier: Identifier


def yield_callables(graph: SemanticGraph) -> Iterable[Callable]:
    for function in graph.basic.functions.values():
        yield function

    for snippet in graph.basic.snippets.values():
        yield snippet


def validate_duplicated_function_names(
    graph: SemanticGraph,
) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []
    seen: Set[bytes] = set()

    for callable in yield_callables(graph):
        if callable.identifier.name in seen:
            diagnostics.append(
                err.report_e3006_duplicated_function_names(
                    callable.ref,
                    callable.identifier.name,
                )
            )
        else:
            seen.add(callable.identifier.name)

    return diagnostics
