from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.binds import Bind, BindId
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.results import ResultId
from i13c.syntax import tree


def configure_binds() -> GraphNode:
    return GraphNode(
        builder=build_binds,
        constraint=None,
        produces=("entities/binds",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_binds(
    graph: SyntaxGraph,
) -> OneToOne[BindId, Bind]:
    binds: dict[BindId, Bind] = {}

    for nid, entry in graph.snippet.binds.items():
        # find the parent slot
        node = graph.snippet.binds.get_ctx(nid)

        if isinstance(node, tree.snippet.Slot):
            id = graph.snippet.slots.get_by_node(node)
            ctx = ParameterId(value=id.value)
            src, dst = node.name, entry.name

        else:
            id = graph.snippet.results.get_by_node(node)
            ctx = ResultId(value=id.value)
            src, dst = b"_ret", entry.name

        # derive bind ID from globally unique node ID
        bind_id = BindId(value=nid.value)

        binds[bind_id] = Bind(
            ref=entry.ref,
            ctx=ctx,
            src=src,
            dst=dst,
        )

    return OneToOne[BindId, Bind].instance(binds)


class ListExtractor:
    def __init__(self, data: OneToOne[BindId, Bind]):
        self.data = data

    def extract(self) -> Iterable[tuple[BindId, Bind]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "ctx": "Context",
            "src": "Source",
            "dst": "Destination",
        }

    @staticmethod
    def rows(key: BindId, entry: Bind) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "ctx": entry.ctx.identify(1),
            "src": entry.src.decode(),
            "dst": entry.dst.decode(),
        }
