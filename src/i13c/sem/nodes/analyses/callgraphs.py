from typing import Dict, List, Set

from i13c.core.mapping import OneToMany, OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.callables import CallableTarget
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.indices.callgraphs import CallPair
from i13c.sem.typing.indices.flowgraphs import FlowGraph, FlowNode


def configure_callgraphs_live() -> Configuration:
    return Configuration(
        builder=build_callgraph_live,
        produces=("analyses/calls-by-caller/live",),
        requires=frozenset(
            {
                ("flowgraphs_live", "analyses/flowgraph-by-function/live"),
                ("callgraph", "indices/calls-by-caller"),
            }
        ),
    )


def build_callgraph_live(
    flowgraphs_live: OneToOne[FunctionId, FlowGraph],
    callgraph: OneToMany[CallableTarget, CallPair],
) -> OneToMany[CallableTarget, CallPair]:
    out: Dict[CallableTarget, List[CallPair]] = {}

    def reachable_nodes(flowgraph: FlowGraph) -> Set[FlowNode]:
        visited: Set[FlowNode] = set()
        stack: List[FlowNode] = [flowgraph.entry]

        while stack:
            node = stack.pop()
            if node in visited:
                continue

            visited.add(node)
            for successor in flowgraph.edges.get(node, []):
                stack.append(successor)

        return visited

    for fid, flowgraph in flowgraphs_live.items():
        live = reachable_nodes(flowgraph)
        out[fid] = [pair for pair in callgraph.get(fid) if pair.callsite in live]

    return OneToMany[CallableTarget, CallPair].instance(out)
