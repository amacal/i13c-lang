from typing import Any

from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.usages import UsageId
from i13c.semantic.typing.identifiers.callsites import CallSiteId
from i13c.semantic.typing.resolutions.expressions import (
    ExpressionAcceptance,
    ExpressionNode,
    ExpressionResolution,
)
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.usages import UsageAcceptance


def configure_expression_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_expression_resolution,
        constraint=None,
        produces=("resolutions/expressions",),
        requires=frozenset(
            {
                ("expressions", "entities/expressions"),
                ("literals", "resolutions/literals/accepted"),
                ("usages", "resolutions/usages/accepted"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_expression_resolution_accepted,
        constraint=None,
        produces=("resolutions/expressions/accepted",),
        requires=frozenset(
            {
                ("resolutions", "resolutions/expressions"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, extract])


def build_expression_resolution(
    expressions: OneToOne[ExpressionId, Expression],
    literals: OneToOne[LiteralId, LiteralAcceptance],
    usages: OneToOne[UsageId, UsageAcceptance],
) -> OneToOne[ExpressionId, ExpressionResolution]:
    resolutions: dict[ExpressionId, ExpressionResolution] = {}

    for eid, entry in expressions.items():
        resolution = ExpressionResolution(
            accepted=[],
            rejected=[],
        )

        nodes: list[ExpressionNode] = []

        for node in entry.nodes:
            if isinstance(node, LiteralId):
                nodes.append(literals.get(node))

            if isinstance(node, UsageId):
                nodes.append(usages.get(node))

            if isinstance(node, CallSiteId):
                nodes.append(node)

        resolution.accepted.append(
            ExpressionAcceptance(
                ref=entry.ref,
                id=eid,
                nodes=nodes,
            )
        )

        resolutions[eid] = resolution

    return OneToOne[ExpressionId, ExpressionResolution].instance(resolutions)


def build_expression_resolution_accepted(
    resolutions: OneToOne[ExpressionId, ExpressionResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[ExpressionId, ExpressionAcceptance]:
    accepted: dict[ExpressionId, ExpressionAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[ExpressionId, ExpressionAcceptance].instance(accepted)
