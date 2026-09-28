from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.results import Result, ResultId
from i13c.semantic.typing.entities.types import TypeId


def configure_results() -> GraphNode:
    return GraphNode(
        builder=build_results,
        constraint=None,
        produces=("entities/results",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_results(
    graph: SyntaxGraph,
) -> OneToOne[ResultId, Result]:
    results: dict[ResultId, Result] = {}

    # first collect all snippet results
    for nid, entry in graph.snippet.results.items():
        # derive parameter ID from globally unique node ID
        result_id = ResultId(value=nid.value)

        # reverse mapping to type ID
        nid = graph.types.get_by_node(entry.type)
        type_id = TypeId(value=nid.value)

        results[result_id] = Result(
            ref=entry.ref,
            type=type_id,
        )

    return OneToOne[ResultId, Result].instance(results)


class ListExtractor:
    def __init__(self, data: OneToOne[ResultId, Result]):
        self.data = data

    def extract(self) -> Iterable[tuple[ResultId, Result]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "type": "Type",
        }

    @staticmethod
    def rows(key: ResultId, entry: Result) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "type": entry.type.identify(1),
        }
