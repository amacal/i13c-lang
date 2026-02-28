from typing import Dict, List

from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.bindings import CallSiteBinding, CallSiteBindings
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.indices.controlflows import FlowNode
from i13c.semantic.typing.indices.environments import Environment
from i13c.semantic.typing.resolutions.callsites import (
    CallSiteAcceptance,
    CallSiteResolution,
)


def configure_bindings() -> GraphNode:
    return GraphNode(
        builder=build_bindings,
        constraint=None,
        produces=("entities/bindings",),
        requires=frozenset(
            {
                ("expressions", "entities/expressions"),
                ("resolutions", "resolutions/callsites"),
                ("environments", "indices/environment-by-flownode"),
            }
        ),
    )


def build_bindings(
    expressions: OneToOne[ExpressionId, Expression],
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
    environments: OneToOne[FlowNode, Environment],
) -> OneToOne[CallSiteId, CallSiteBindings]:

    bindings: Dict[CallSiteId, CallSiteBindings] = {}

    for cid, resolution in resolutions.items():
        for acceptance in resolution.accepted:
            environment = environments.get(cid)
            bindings[cid] = CallSiteBindings(
                callable=acceptance.callable,
                bindings=transform_bindings(expressions, acceptance, environment),
            )

    return OneToOne[CallSiteId, CallSiteBindings](data=bindings)


def transform_bindings(
    expressions: OneToOne[ExpressionId, Expression],
    acceptance: CallSiteAcceptance,
    environment: Environment,
) -> List[CallSiteBinding]:
    bindings: List[CallSiteBinding] = []

    for binding in acceptance.bindings:
        if binding.argument.kind == b"literal":
            assert isinstance(binding.argument.target, LiteralId)
            bindings.append(CallSiteBinding(target=binding.argument.target))

        elif binding.argument.kind == b"expression":
            assert isinstance(binding.argument.target, ExpressionId)
            expression = expressions.get(binding.argument.target)

            assert expression.ident in environment.variables
            variable = environment.variables[expression.ident]

            bindings.append(CallSiteBinding(target=variable))

    return bindings
