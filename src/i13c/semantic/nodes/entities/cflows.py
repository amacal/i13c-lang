from typing import Dict, List

from i13c.core.generator import Generator
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.cflows import (
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
        produces=("entities/cflows",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("graph", "syntax/graph"),
            }
        ),
    )


def build_control_flows(
    generator: Generator,
    graph: SyntaxGraph,
) -> OneToOne[FunctionId, ControlFlows]:
    cflows: Dict[FunctionId, ControlFlows] = {}

    for nid, node in graph.function.functions.items():
        # derive function ID from globally unique node ID
        function_id = FunctionId(value=nid.value)

        entry = FlowEntry(value=generator.next())
        exit = FlowExit(value=generator.next())

        nodes: List[FlowMember] = [entry]
        forward: Dict[int, List[int]] = {}
        backward: Dict[int, List[int]] = {}

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

        for idx in range(0, len(nodes)):
            backward[idx] = []

        for start, ends in forward.items():
            for end in ends:
                backward[end].append(start)

        for start in list(backward.keys()):
            if not backward[start]:
                del backward[start]

        cflows[function_id] = ControlFlows(
            ref=node.ref,
            target=function_id,
            nodes=nodes,
            forward=forward,
            backward=backward,
        )

    return OneToOne[FunctionId, ControlFlows].instance(cflows)
