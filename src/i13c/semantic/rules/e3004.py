from typing import List, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.syntax.source import SpanLike


def configure_e3004() -> GraphNode:
    return GraphNode(
        builder=validate_duplicated_parameter_names,
        constraint=None,
        produces=("rules/e3004",),
        requires=frozenset(
            {
                ("snippets", "entities/snippets"),
                ("functions", "entities/functions"),
                ("parameters", "entities/parameters"),
            }
        ),
    )


def validate_duplicated_parameter_names(
    snippets: OneToOne[SnippetId, Snippet],
    functions: OneToOne[FunctionId, Function],
    parameters: OneToOne[ParameterId, Parameter],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for snippet in snippets.values():
        seen: Set[bytes] = set()

        for slot in snippet.slots:
            if slot.name.data in seen:
                diagnostics.append(
                    report_e3004_duplicated_parameter_names(snippet.ref, slot.name.data)
                )
            else:
                seen.add(slot.name.data)

    for function in functions.values():
        seen: Set[bytes] = set()

        for pid in function.parameters:
            parameter = parameters.get(pid)

            if parameter.ident.data in seen:
                diagnostics.append(
                    report_e3004_duplicated_parameter_names(
                        function.ref, parameter.ident.data
                    )
                )
            else:
                seen.add(parameter.ident.data)

    return diagnostics


def report_e3004_duplicated_parameter_names(ref: SpanLike, found: bytes) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E3004",
        message=f"Duplicated parameter names for ({str(found)}) at offset {ref.offset}",
    )
