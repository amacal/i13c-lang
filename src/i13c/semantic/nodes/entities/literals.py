from collections.abc import Iterable

from i13c.core.graph import AbstractListExtractor, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.literals import Hex, Literal, LiteralId


def configure_literals() -> GraphNode:
    return GraphNode(
        builder=build_literals,
        constraint=None,
        produces=("entities/literals",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=list_literals),
    )


def build_literals(
    graph: SyntaxGraph,
) -> OneToOne[LiteralId, Literal]:
    literals: dict[LiteralId, Literal] = {}

    for nid, literal in graph.function.literals.items():
        # derive literal ID from globally unique node ID
        literal_id = LiteralId(value=nid.value)

        literals[literal_id] = Literal(
            ref=literal.ref,
            target=Hex.derive(literal.value.digits),
        )

    return OneToOne[LiteralId, Literal].instance(literals)


class ListExtractor:
    def __init__(self, data: OneToOne[LiteralId, Literal]):
        self.data = data

    def extract(self) -> Iterable[tuple[LiteralId, Literal]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "value": "Value",
            "width": "Width",
        }

    @staticmethod
    def rows(key: LiteralId, entry: Literal) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "value": str(entry.target),
            "width": str(entry.target.width),
        }


def list_literals(
    data: OneToOne[LiteralId, Literal],
) -> AbstractListExtractor[LiteralId, Literal]:
    return ListExtractor(data)
