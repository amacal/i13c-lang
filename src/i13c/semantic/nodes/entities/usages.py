from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.usages import Usage
from i13c.semantic.typing.identifiers.functions import FunctionId
from i13c.semantic.typing.identifiers.statements import StatementId
from i13c.semantic.typing.identifiers.usages import UsageId


def configure_usages() -> GraphNode:
    return GraphNode(
        builder=build_usages,
        constraint=None,
        produces=("entities/usages",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_usages(
    graph: SyntaxGraph,
) -> OneToOne[UsageId, Usage]:
    usages: dict[UsageId, Usage] = {}

    for nid, usage in graph.function.usages.items():
        # derive usage ID from globally unique node ID
        usage_id = UsageId(value=nid.value)

        # find the owning statement of this usage
        stmt = graph.function.usages.get_ctx(nid)
        stmt_nid = graph.function.statements.get_by_node(stmt)

        # find the owning function of this usage
        fn = graph.function.statements.get_ctx(stmt_nid)
        fn_nid = graph.function.functions.get_by_node(fn)

        usages[usage_id] = Usage(
            ref=usage.ref,
            name=usage.name,
            statement=stmt_nid,
            function=fn_nid,
        )

    return OneToOne[UsageId, Usage].instance(usages)


class ListExtractor:
    def __init__(self, data: OneToOne[UsageId, Usage]):
        self.data = data

    def extract(self) -> Iterable[tuple[UsageId, Usage]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "fn": "Function",
            "stmt": "Statement",
        }

    @staticmethod
    def rows(key: UsageId, entry: Usage) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "fn": entry.get_function(FunctionId.from_context).identify(1),
            "stmt": entry.get_statement(StatementId.from_context).identify(1),
        }
