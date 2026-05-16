from typing import Dict, List

from i13c.core.graph import GraphNode
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
    )


def build_functions(
    graph: SyntaxGraph,
) -> OneToOne[FunctionId, Function]:
    functions: Dict[FunctionId, Function] = {}

    for nid, node in graph.function.functions.items():
        # derive function ID from globally unique node ID
        function_id = FunctionId(value=nid.value)
        statements: List[StatementId] = []

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
            signature=signature_id,
            flags=flags_id,
            statements=statements,
        )

    return OneToOne[FunctionId, Function].instance(functions)
