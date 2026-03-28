from typing import Iterable, List, Protocol, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Identifier
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.syntax.source import Span, SpanLike


def configure_e3006() -> GraphNode:
    return GraphNode(
        builder=validate_duplicated_function_names,
        constraint=None,
        produces=("rules/e3006",),
        requires=frozenset(
            {("functions", "entities/functions"), ("snippets", "entities/snippets")}
        ),
    )


class Callable(Protocol):
    ref: Span
    identifier: Identifier


def yield_callables(
    functions: OneToOne[FunctionId, Function],
    snippets: OneToOne[SnippetId, Snippet],
) -> Iterable[Callable]:
    for function in functions.values():
        yield function

    for snippet in snippets.values():
        yield snippet


def validate_duplicated_function_names(
    functions: OneToOne[FunctionId, Function],
    snippets: OneToOne[SnippetId, Snippet],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []
    seen: Set[bytes] = set()

    for callable in yield_callables(functions, snippets):
        if callable.identifier.name in seen:
            diagnostics.append(
                report_e3006_duplicated_function_names(
                    callable.ref,
                    callable.identifier.name,
                )
            )
        else:
            seen.add(callable.identifier.name)

    return diagnostics


def report_e3006_duplicated_function_names(
    ref: SpanLike, found: bytes
) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E3006",
        message=f"Duplicated function names for ({str(found)}) at offset {ref.offset}",
    )
