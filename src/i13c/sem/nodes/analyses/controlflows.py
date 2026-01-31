from typing import Dict, List, Set

from i13c.core.mapping import OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.callables import CallableTarget
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.entities.snippets import Snippet, SnippetId
from i13c.sem.typing.indices.controlflows import FlowGraph, FlowNode
from i13c.sem.typing.indices.terminalities import Terminality
from i13c.sem.typing.resolutions.callsites import CallSiteResolution


def configure_flowgraphs_live() -> Configuration:
    return Configuration(
        builder=build_flowgraphs_live,
        produces=("analyses/flowgraph-by-function/live",),
        requires=frozenset(
            {
                ("flowgraph_by_function", "indices/flowgraph-by-function"),
                ("resolutions", "resolutions/callsites"),
                ("snippets", "entities/snippets"),
                ("terminalities", "indices/terminality-by-function"),
            }
        ),
    )


def prune_flowgraph(
    flowgraph: FlowGraph,
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
    noreturn: Set[CallableTarget],
) -> FlowGraph:
    forward: Dict[FlowNode, List[FlowNode]] = {}
    backward: Dict[FlowNode, List[FlowNode]] = {}

    for node in flowgraph.backward.keys():
        backward[node] = []

    for node, successors in flowgraph.forward.items():
        if isinstance(node, CallSiteId):
            # node is a callsite
            resolution = resolutions.get(node)
            acceptable = False

            # no accepted callables, all successors are pruned
            if not resolution.accepted:
                successors = []

            # check if any accepted callable is not noreturn
            for accepted in resolution.accepted:
                if accepted.callable.target not in noreturn:
                    acceptable = True
                    break

            # all accepted callables are noreturn, prune successors
            if not acceptable:
                successors = []

        # register successors
        forward[node] = list(successors)

        # register backwards edges
        for successor in successors:
            backward[successor].append(node)

    queue: List[FlowNode] = [flowgraph.entry]
    visited: Set[FlowNode] = set()

    while queue:
        node = queue.pop()
        if node in visited:
            continue

        visited.add(node)

        for successor in forward.get(node, []):
            if successor not in visited:
                queue.append(successor)

    # prune forward edges to visited nodes only
    forward = {
        node: [s for s in successors if s in visited]
        for node, successors in forward.items()
        if node in visited
    }

    # prune backward edges to visited nodes only
    backward = {
        node: [p for p in predecessors if p in visited]
        for node, predecessors in backward.items()
        if node in visited
    }

    # let's be sure entry is still there
    assert flowgraph.entry in forward

    return FlowGraph(
        entry=flowgraph.entry,
        exit=flowgraph.exit,
        forward=forward,
        backward=backward,
    )


def build_flowgraphs_live(
    flowgraph_by_function: OneToOne[FunctionId, FlowGraph],
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
    snippets: OneToOne[SnippetId, Snippet],
    terminalities: OneToOne[FunctionId, Terminality],
) -> OneToOne[FunctionId, FlowGraph]:
    out: Dict[FunctionId, FlowGraph] = {}
    noreturn: Set[CallableTarget] = set()

    for fid, terminality in terminalities.items():
        if terminality.noreturn:
            noreturn.add(fid)

    for snid, snippet in snippets.items():
        if snippet.noreturn:
            noreturn.add(snid)

    for fid, flowgraph in flowgraph_by_function.items():
        out[fid] = prune_flowgraph(flowgraph, resolutions, noreturn)

    return OneToOne[FunctionId, FlowGraph].instance(out)
