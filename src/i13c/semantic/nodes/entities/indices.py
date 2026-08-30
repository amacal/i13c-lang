from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.indices import Index, IndexId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax import tree


def configure_indices() -> GraphNode:
    return GraphNode(
        builder=build_indices,
        constraint=None,
        produces=("entities/indices",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_indices(
    graph: SyntaxGraph,
) -> OneToOne[IndexId, Index]:
    indices: dict[IndexId, Index] = {}

    for nid, entry in graph.snippet.indices.items():
        # derive index ID from globally unique node ID
        index_id = IndexId(value=nid.value)

        if isinstance(entry.target, tree.snippet.Register):
            target_nid = graph.snippet.registers.get_by_node(entry.target)
            target_id = RegisterId(value=target_nid.value)
        else:
            target_nid = graph.snippet.references.get_by_node(entry.target)
            target_id = ReferenceId(value=target_nid.value)

        indices[index_id] = Index(
            ref=entry.ref,
            scale=entry.scale,
            target=target_id,
        )

    return OneToOne[IndexId, Index].instance(indices)


class ListExtractor:
    def __init__(self, data: OneToOne[IndexId, Index]):
        self.data = data

    def extract(self) -> Iterable[tuple[IndexId, Index]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "target": "Target",
        }

    @staticmethod
    def rows(key: IndexId, entry: Index) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "target": key.identify(1),
        }
