from typing import List

from i13c import err
from i13c.core import diagnostics
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.callables import CallableTarget
from i13c.semantic.typing.indices.entrypoints import EntryPoint


def configure_e3011() -> GraphNode:
    return GraphNode(
        builder=validate_entrypoint_exists,
        constraint=None,
        produces=("rules/e3011",),
        requires=frozenset({("entrypoints", "indices/entrypoints-by-callable")}),
    )


def validate_entrypoint_exists(
    entrypoints: OneToOne[CallableTarget, EntryPoint],
) -> List[diagnostics.Diagnostic]:

    if entrypoints.size() > 0:
        return []

    return [err.report_e3011_missing_entrypoint_function()]
