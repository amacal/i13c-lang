from typing import Dict

from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Identifier, Range, Type, default_range, width_from_range
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId


def configure_parameters() -> GraphNode:
    return GraphNode(
        builder=build_parameters,
        produces=("entities/parameters",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_parameters(
    graph: SyntaxGraph,
) -> OneToOne[ParameterId, Parameter]:
    parameters: Dict[ParameterId, Parameter] = {}

    for pid, parameter in graph.parameters.items():
        # derive parameter ID from globally unique node ID
        parameter_id = ParameterId(value=pid.value)

        # default width and ranges for declared type
        range: Range = default_range(parameter.type.name)

        # override ranges if specified
        if parameter.type.range is not None:
            range = Range(
                lower=parameter.type.range.lower,
                upper=parameter.type.range.upper,
            )

        # derive width from ranges
        width = width_from_range(range)

        # construct slot type with range or default width
        type = Type(
            name=parameter.type.name,
            width=width,
            range=range,
        )

        parameters[parameter_id] = Parameter(
            ref=parameter.ref,
            type=type,
            ident=Identifier(name=parameter.name),
        )

    return OneToOne[ParameterId, Parameter].instance(parameters)
