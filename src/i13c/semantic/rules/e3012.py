from typing import List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.callables import CallableTarget
from i13c.semantic.typing.indices.entrypoints import EntryPoint
from i13c.syntax.source import Span


def configure_e3012() -> GraphNode:
    return GraphNode(
        builder=validate_entrypoint_is_single,
        constraint=None,
        produces=("rules/e3012",),
        requires=frozenset({("entrypoints", "indices/entrypoints-by-callable")}),
    )


def validate_entrypoint_is_single(
    entrypoints: OneToOne[CallableTarget, EntryPoint],
) -> List[Diagnostic]:

    if entrypoints.size() <= 1:
        return []

    return [report_e3012_multiple_entrypoint_functions()]


def report_e3012_multiple_entrypoint_functions() -> Diagnostic:
    return Diagnostic(
        ref=Span(offset=0, length=0),
        code="E3012",
        message="Multiple entrypoint codeblocks found",
    )
