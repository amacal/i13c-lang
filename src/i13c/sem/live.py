from typing import Dict, List, Set

from i13c.sem.callable import CallableTarget
from i13c.sem.callgraphs import CallGraphs
from i13c.sem.callsite import CallSiteId
from i13c.sem.entrypoint import EntryPoint
from i13c.sem.flowgraphs import FlowGraph, FlowNode
from i13c.sem.function import FunctionId
from i13c.sem.resolve import Resolution
from i13c.sem.snippet import Snippet, SnippetId
from i13c.sem.terminal import Terminality


def build_callgraph_live(
    flowgraphs_live: Dict[FunctionId, FlowGraph], callgraph: CallGraphs
) -> CallGraphs:
    out: CallGraphs = {}

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
        out[fid] = [(cid, callee) for (cid, callee) in callgraph[fid] if cid in live]

    return out


def build_callable_live(
    entrypoints: List[EntryPoint],
    callgraph_live: CallGraphs,
) -> Set[CallableTarget]:
    out: Set[CallableTarget] = set()
    stack: List[CallableTarget] = []

    for entrypoint in entrypoints:
        out.add(entrypoint.target)
        stack.append(entrypoint.target)

    while stack:
        for _, target in callgraph_live.get(stack.pop(), []):
            if isinstance(target, FunctionId):
                if target not in out:
                    stack.append(target)
                    out.add(target)

    return out


def prune_flowgraph(
    flowgraph: FlowGraph,
    resolutions: Dict[CallSiteId, Resolution],
    noreturn: Set[CallableTarget],
) -> FlowGraph:
    edges: Dict[FlowNode, List[FlowNode]] = {}

    for node, successors in flowgraph.edges.items():
        if isinstance(node, CallSiteId):
            # node is a callsite
            resolution = resolutions[node]
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

        edges[node] = list(successors)

    queue: List[FlowNode] = [flowgraph.entry]
    visited: Set[FlowNode] = set()

    while queue:
        node = queue.pop()
        if node in visited:
            continue

        visited.add(node)

        for successor in edges.get(node, []):
            if successor not in visited:
                queue.append(successor)

    # prune edges to visited nodes only
    edges = {
        node: [s for s in successors if s in visited]
        for node, successors in edges.items()
        if node in visited
    }

    # let's be sure entry is still there
    assert flowgraph.entry in edges

    return FlowGraph(
        entry=flowgraph.entry,
        exit=flowgraph.exit,
        edges=edges,
    )


def build_flowgraphs_live(
    function_flowgraphs: Dict[FunctionId, FlowGraph],
    resolutions: Dict[CallSiteId, Resolution],
    snippets: Dict[SnippetId, Snippet],
    terminalities: Dict[FunctionId, Terminality],
) -> Dict[FunctionId, FlowGraph]:
    out: Dict[FunctionId, FlowGraph] = {}
    noreturn: Set[CallableTarget] = set()

    for fid, terminality in terminalities.items():
        if terminality.noreturn:
            noreturn.add(fid)

    for snid, snippet in snippets.items():
        if snippet.noreturn:
            noreturn.add(snid)

    for fid, flowgraph in function_flowgraphs.items():
        out[fid] = prune_flowgraph(flowgraph, resolutions, noreturn)

    return out
