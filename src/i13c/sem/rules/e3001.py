from typing import Iterator, List, Tuple

from i13c import diag, err
from i13c.sem.core import Type, default_ranges
from i13c.sem.model import SemanticGraph
from i13c.src import Span


def iterate_candidates(graph: SemanticGraph) -> Iterator[Tuple[Span, Type]]:
    for snippet in graph.basic.snippets.values():
        for slot in snippet.slots:
            yield snippet.ref, slot.type

    for function in graph.basic.functions.values():
        for parameter in function.parameters:
            yield function.ref, parameter.type


def validate_type_ranges(graph: SemanticGraph) -> List[diag.Diagnostic]:
    diagnostics: List[diag.Diagnostic] = []

    for ref, type in iterate_candidates(graph):
        defaults = default_ranges(type.name)

        if type.lower > type.upper:
            diagnostics.append(
                err.report_e3001_invalid_type_ranges(ref, type.lower, type.upper)
            )

        if type.lower < defaults[0] or type.upper > defaults[1]:
            diagnostics.append(
                err.report_e3001_invalid_type_ranges(ref, type.lower, type.upper)
            )

    return diagnostics
