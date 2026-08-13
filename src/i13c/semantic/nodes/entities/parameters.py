from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
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
        views=GraphViews(list=ListExtractor),
    )


def build_parameters(
    graph: SyntaxGraph,
) -> OneToOne[ParameterId, Parameter]:
    parameters: dict[ParameterId, Parameter] = {}

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


class ListExtractor:
    def __init__(self, data: OneToOne[ParameterId, Parameter]):
        self.data = data

    def extract(self) -> Iterable[tuple[ParameterId, Parameter]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "type": "Type",
        }

    @staticmethod
    def rows(key: ParameterId, entry: Parameter) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "type": entry.type.identify(1),
        }
