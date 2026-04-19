from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.types import TypeId


def configure_parameters() -> GraphNode:
    return GraphNode(
        builder=build_parameters,
        constraint=None,
        produces=("entities/parameters",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_parameters(
    graph: SyntaxGraph,
) -> OneToOne[ParameterId, Parameter]:
    parameters: Dict[ParameterId, Parameter] = {}

    # first collect all snippet slots as parameters
    for nid, entry in graph.snippet.slots.items():
        # derive parameter ID from globally unique node ID
        parameter_id = ParameterId(value=nid.value)

        # reverse mapping to type ID
        nid = graph.types.get_by_node(entry.type)
        type_id = TypeId(value=nid.value)

        parameters[parameter_id] = Parameter(
            ref=entry.ref,
            name=entry.name,
            type=type_id,
        )

    # then collect all regular function parameters
    for nid, entry in graph.function.parameters.items():
        # derive parameter ID from globally unique node ID
        parameter_id = ParameterId(value=nid.value)

        # reverse mapping to type ID
        nid = graph.types.get_by_node(entry.type)
        type_id = TypeId(value=nid.value)

        parameters[parameter_id] = Parameter(
            ref=entry.ref,
            name=entry.name,
            type=type_id,
        )

    return OneToOne[ParameterId, Parameter].instance(parameters)
