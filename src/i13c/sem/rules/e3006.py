from typing import Iterable, List, Protocol, Set

from i13c import diag, err
from i13c.sem.core import Identifier
from i13c.sem.model import SemanticGraph
from i13c.src import Span


class Callable(Protocol):
    ref: Span
    identifier: Identifier


def yield_callables(graph: SemanticGraph) -> Iterable[Callable]:
    for function in graph.functions.values():
        yield function

    for snippet in graph.snippets.values():
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
