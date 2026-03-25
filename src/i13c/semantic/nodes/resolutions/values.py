from typing import Dict, Optional

from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.entities.literals import Literal, LiteralId
from i13c.semantic.typing.entities.values import Value, ValueId
from i13c.semantic.typing.indices.controlflows import FlowNode
from i13c.semantic.typing.indices.environments import Environment
from i13c.semantic.typing.indices.variables import Variable, VariableId
from i13c.semantic.typing.resolutions.values import (
    ValueAcceptance,
    ValueBinding,
    ValueRejection,
    ValueRejectionReason,
    ValueResolution,
)


def configure_resolution_by_value() -> GraphNode:
    return GraphNode(
        builder=build_resolution_by_value,
        constraint=None,
        produces=("resolutions/values",),
        requires=frozenset(
            {
                ("values", "entities/values"),
                ("literals", "entities/literals"),
                ("variables", "entities/variables"),
                ("expressions", "entities/expressions"),
                ("environments", "indices/environment-by-flownode"),
            }
        ),
    )


def build_resolution_by_value(
    values: OneToOne[ValueId, Value],
    literals: OneToOne[LiteralId, Literal],
    variables: OneToOne[VariableId, Variable],
    expressions: OneToOne[ExpressionId, Expression],
    environments: OneToOne[FlowNode, Environment],
) -> OneToOne[ValueId, ValueResolution]:
    resolutions: Dict[ValueId, ValueResolution] = {}

    for value in values.values():
        binding: Optional[ValueBinding] = None
        reason: Optional[ValueRejectionReason] = None

        if isinstance(value.expr.target, LiteralId):
            if not literals.get(value.expr.target).fits(value.type):
                reason = b"type-mismatch"
            else:
                binding = value.expr.target

        if isinstance(value.expr.target, ExpressionId):
            # environment and expression must exist
            environment = environments.get(value.id)
            expression = expressions.get(value.expr.target)

            # variable may not exist if unknown identifier is used
            if variable := environment.variables.get(expression.ident):
                if not value.type.accepts(variables.get(variable).type):
                    reason = b"type-mismatch"

                else:
                    binding = variable

            else:
                reason = b"unbound"

        # only one of binding or reason can be set
        assert not (binding and reason)

        if binding:
            resolutions[value.id] = ValueResolution(
                accepted=ValueAcceptance(binding=binding),
                rejected=None,
            )

        if reason:
            resolutions[value.id] = ValueResolution(
                accepted=None,
                rejected=ValueRejection(reason=reason),
            )

    return OneToOne[ValueId, ValueResolution].instance(resolutions)
