from typing import Iterator, List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Hex, Type, default_range
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.syntax.source import Span, SpanLike


def configure_e3001() -> GraphNode:
    return GraphNode(
        builder=validate_type_ranges,
        constraint=None,
        produces=("rules/e3001",),
        requires=frozenset(
            {
                ("snippets", "entities/snippets"),
                ("functions", "entities/functions"),
                ("parameters", "entities/parameters"),
            }
        ),
    )


def iterate_candidates(
    snippets: OneToOne[SnippetId, Snippet],
    functions: OneToOne[FunctionId, Function],
    parameters: OneToOne[ParameterId, Parameter],
) -> Iterator[Tuple[Span, Type]]:
    for snippet in snippets.values():
        for slot in snippet.slots:
            yield snippet.ref, slot.type

    for function in functions.values():
        for pid in function.parameters:
            yield function.ref, parameters.get(pid).type


def validate_type_ranges(
    snippets: OneToOne[SnippetId, Snippet],
    functions: OneToOne[FunctionId, Function],
    parameters: OneToOne[ParameterId, Parameter],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for ref, type in iterate_candidates(snippets, functions, parameters):
        defaults = default_range(type.name)

        if Hex.greater(type.range.lower.data, type.range.upper.data):
            diagnostics.append(
                report_e3001_invalid_type_ranges(
                    ref, type.range.lower, type.range.upper
                )
            )

        elif Hex.lesser(type.range.lower.data, defaults.lower.data) or Hex.greater(
            type.range.upper.data, defaults.upper.data
        ):
            diagnostics.append(
                report_e3001_invalid_type_ranges(
                    ref, type.range.lower, type.range.upper
                )
            )

    return diagnostics


def report_e3001_invalid_type_ranges(
    ref: SpanLike, lower: Hex, upper: Hex
) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E3001",
        message=f"Invalid type ranges [{lower}..{upper}] at offset {ref.offset}",
    )
