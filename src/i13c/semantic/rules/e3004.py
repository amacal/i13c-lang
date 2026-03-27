from typing import List, Set

from i13c import err
from i13c.core import diagnostics
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId


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
) -> List[diagnostics.Diagnostic]:
    diagnostics: List[diagnostics.Diagnostic] = []

    for snippet in snippets.values():
        seen: Set[bytes] = set()

        for slot in snippet.slots:
            if slot.name.name in seen:
                diagnostics.append(
                    err.report_e3004_duplicated_parameter_names(
                        snippet.ref, slot.name.name
                    )
                )
            else:
                seen.add(slot.name.name)

    for function in functions.values():
        seen: Set[bytes] = set()

        for pid in function.parameters:
            parameter = parameters.get(pid)

            if parameter.ident.name in seen:
                diagnostics.append(
                    err.report_e3004_duplicated_parameter_names(
                        function.ref, parameter.ident.name
                    )
                )
            else:
                seen.add(parameter.ident.name)

    return diagnostics
