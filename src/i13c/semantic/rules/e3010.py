from typing import List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.indices.terminalities import Terminality
from i13c.syntax.source import SpanLike


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
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for fid, terminality in terminalities.items():
        # we need to compare against the function definition
        function = functions.get(fid)

        # if the terminality expectations do not match, report an error
        if function.noreturn != terminality.noreturn:
            diagnostics.append(
                report_e3010_function_has_wrong_terminality(
                    function.ref,
                    function.identifier.data,
                )
            )

    return diagnostics


def report_e3010_function_has_wrong_terminality(
    ref: SpanLike, name: bytes
) -> Diagnostic:
    return Diagnostic(
        ref=ref,
        code="E3010",
        message=f"Function '{str(name)}' has wrong terminality: does not match declaration",
    )
