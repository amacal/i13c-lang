from collections.abc import Iterable

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.statements import StatementId


def configure_functions() -> GraphNode:
    return GraphNode(
        builder=build_functions,
        constraint=None,
        produces=("entities/functions",),
        requires=frozenset({("graph", "syntax/graph")}),
        views=GraphViews(list=ListExtractor),
    )


def build_functions(
    graph: SyntaxGraph,
) -> OneToOne[FunctionId, Function]:
    functions: dict[FunctionId, Function] = {}

    for nid, node in graph.function.functions.items():
        # derive function ID from globally unique node ID
        function_id = FunctionId(value=nid.value)
        statements: list[StatementId] = []

        # identify signature ID from globally unique node ID
        nid = graph.function.signatures.get_by_node(node.signature)
        signature_id = SignatureId(value=nid.value)

        # identify flags ID from globally unique node ID
        if node.flags is not None:
            nid = graph.function.flags.get_by_node(node.flags)
            flags_id = FlagsId(value=nid.value)
        else:
            flags_id = None

        for statement in node.statements:
            nid = graph.function.statements.get_by_node(statement)
            statements.append(StatementId(value=nid.value))

        functions[function_id] = Function(
            ref=node.ref,
            id=function_id,
            signature=signature_id,
            flags=flags_id,
            statements=statements,
        )

    return OneToOne[FunctionId, Function].instance(functions)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, Function]):
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, Function]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "sig": "Signature",
            "flags": "Flags",
            "stmts": "Statements",
        }

    @staticmethod
    def rows(key: FunctionId, entry: Function) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "sig": entry.signature.identify(1),
            "flags": entry.flags.identify(1) if entry.flags else "",
            "stmts": str(len(entry.statements)),
        }
