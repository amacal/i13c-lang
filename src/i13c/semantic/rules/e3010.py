from typing import List

from i13c import err
from i13c.core import diagnostics
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.indices.terminalities import Terminality


def configure_e3010() -> GraphNode:
    return GraphNode(
        builder=validate_called_symbol_terminality,
        constraint=None,
        produces=("rules/e3010",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("terminalities", "indices/terminality-by-function"),
            }
        ),
    )


def validate_called_symbol_terminality(
    functions: OneToOne[FunctionId, Function],
    terminalities: OneToOne[FunctionId, Terminality],
) -> List[diagnostics.Diagnostic]:
    diagnostics: List[diagnostics.Diagnostic] = []

    for fid, terminality in terminalities.items():
        # we need to compare against the function definition
        function = functions.get(fid)

        # if the terminality expectations do not match, report an error
        if function.noreturn != terminality.noreturn:
            diagnostics.append(
                err.report_e3010_function_has_wrong_terminality(
                    function.ref,
                    function.identifier.name,
                )
            )

    return diagnostics
