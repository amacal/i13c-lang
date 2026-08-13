from collections.abc import Iterable

from i13c.core.generator import Generator
from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.analyses.cflows import (
    ControlFlows,
    FlowEntry,
    FlowExit,
    FlowMember,
    FlowNode,
)
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.statements import StatementId


def configure_control_flows() -> GraphNode:
    return GraphNode(
        builder=build_control_flows,
        constraint=None,
        produces=("analyses/cflows",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("graph", "syntax/graph"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_control_flows(
    generator: Generator,
    graph: SyntaxGraph,
) -> OneToOne[FunctionId, ControlFlows]:
    cflows: dict[FunctionId, ControlFlows] = {}

    for nid, node in graph.function.functions.items():
        # derive function ID from globally unique node ID
        function_id = FunctionId(value=nid.value)

        entry = FlowEntry(value=generator.next())
        exit = FlowExit(value=generator.next())

        nodes: list[FlowMember] = [entry]
        forward: dict[int, list[int]] = {}
        backward: dict[int, list[int]] = {}

        prev: int = 0
        for stmt in node.statements:
            nid = graph.function.statements.get_by_node(stmt)
            target = StatementId(value=nid.value)

            flow = FlowNode(target=target)
            forward[prev] = [len(nodes)]

            prev = len(nodes)
            nodes.append(flow)

        forward[prev] = [len(nodes)]
        nodes.append(exit)

        for idx in range(len(nodes)):
            backward[idx] = []

        for start, ends in forward.items():
            for end in ends:
                backward[end].append(start)

        for start in list(backward.keys()):
            if not backward[start]:
                del backward[start]

        cflows[function_id] = ControlFlows(
            ref=node.ref,
            entry=0,
            exit=len(nodes) - 1,
            target=function_id,
            nodes=nodes,
            forward=forward,
            backward=backward,
        )

    return OneToOne[FunctionId, ControlFlows].instance(cflows)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, ControlFlows]):
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, ControlFlows]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "nodes": "Nodes",
            "forward": "Forward",
            "backward": "Backward",
        }

    @staticmethod
    def rows(key: FunctionId, entry: ControlFlows) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "fn": key.identify(1),
            "nodes": str(len(entry.nodes)),
            "forward": str(len(entry.forward)),
            "backward": str(len(entry.backward)),
        }
