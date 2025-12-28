from functools import partial
from typing import Callable as Functor
from typing import Dict, List, Set, Tuple

from i13c.sem.callable import Callable, CallableTarget
from i13c.sem.callsite import CallSiteId
from i13c.sem.entrypoint import EntryPoint
from i13c.sem.flowgraphs import FlowGraph, FlowNode
from i13c.sem.function import FunctionId
from i13c.sem.resolve import Resolution
from i13c.sem.snippet import Snippet, SnippetId
from i13c.sem.terminal import Terminality


def is_callable_terminal(
    snippets: Dict[SnippetId, Snippet],
    terminalities: Dict[FunctionId, Terminality],
    callable: Callable,
) -> bool:

    match callable.target:
        case FunctionId() as fid:
            return terminalities[fid].noreturn
        case SnippetId():
            return snippets[callable.target].noreturn


def is_callsite_terminal(
    snippets: Dict[SnippetId, Snippet],
    terminalities: Dict[FunctionId, Terminality],
    resolutions: Dict[CallSiteId, Resolution],
    cid: CallSiteId,
) -> bool:
    resolution = resolutions[cid]

    for accepted in resolution.accepted:
        if not is_callable_terminal(snippets, terminalities, accepted.callable):
            return False

    return True


def is_callsites_live(
    flowgraph: FlowGraph,
    is_terminal: Functor[[CallSiteId], bool],
) -> List[CallSiteId]:

    out: List[CallSiteId] = []
    visited: Set[FlowNode] = set()
    stack: List[FlowNode] = [flowgraph.entry]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        else:
            visited.add(node)

        if isinstance(node, CallSiteId):
            out.append(node)

            # prune successors
            if is_terminal(node):
                continue

        # enqueue successors, [] for exit node
        for successor in flowgraph.edges.get(node, []):
            stack.append(successor)

    return out


def build_callgraph_live(
    entrypoints: List[EntryPoint],
    snippets: Dict[SnippetId, Snippet],
    flowgraphs: Dict[FunctionId, FlowGraph],
    callgraph: Dict[CallableTarget, List[Tuple[CallSiteId, CallableTarget]]],
    terminalities: Dict[FunctionId, Terminality],
    resolutions: Dict[CallSiteId, Resolution],
) -> Dict[CallableTarget, List[Tuple[CallSiteId, CallableTarget]]]:

    out: Dict[CallableTarget, List[Tuple[CallSiteId, CallableTarget]]] = {}
    stack: List[CallableTarget] = [entrypoint.target for entrypoint in entrypoints]

    while stack:
        target = stack.pop()
        if target in out:
            continue

        reached: List[Tuple[CallSiteId, CallableTarget]] = []

        # shorten is_callsite_terminal function
        is_terminal_args = (snippets, terminalities, resolutions)
        is_terminal = partial(is_callsite_terminal, *is_terminal_args)

        # only functions have flowgraphs
        if isinstance(target, FunctionId):
            callsites = is_callsites_live(flowgraphs[target], is_terminal)
            edges: Dict[CallSiteId, List[CallableTarget]] = {}

            for cid, callee in callgraph[target]:
                edges.setdefault(cid, []).append(callee)

            for cid in callsites:
                # fallback to empty list on exit node
                for callee in edges.get(cid, []):
                    reached.append((cid, callee))
                    stack.append(callee)

        out[target] = reached

    return out


def build_callable_live(
    entrypoints: List[EntryPoint],
    callgraph_live: Dict[CallableTarget, List[Tuple[CallSiteId, CallableTarget]]],
) -> Set[CallableTarget]:
    out: Set[CallableTarget] = set()

    for entrypoint in entrypoints:
        out.add(entrypoint.target)

    for edges in callgraph_live.values():
        for _, target in edges:
            if isinstance(target, FunctionId):
                out.add(target)

    return out
