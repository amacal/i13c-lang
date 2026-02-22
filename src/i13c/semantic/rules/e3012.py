from typing import List

from i13c import diag, err
from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.callables import CallableTarget
from i13c.semantic.typing.indices.entrypoints import EntryPoint


def configure_e3012() -> GraphNode:
    return GraphNode(
        builder=validate_entrypoint_is_single,
        constraint=None,
        produces=("rules/e3012",),
        requires=frozenset({("entrypoints", "indices/entrypoints-by-callable")}),
    )


def validate_entrypoint_is_single(
    entrypoints: OneToOne[CallableTarget, EntryPoint],
) -> List[diag.Diagnostic]:

    if entrypoints.size() <= 1:
        return []

    return [err.report_e3012_multiple_entrypoint_functions()]
