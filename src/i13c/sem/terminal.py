from dataclasses import dataclass
from typing import Dict, List, Set

from i13c.sem.callable import Callable
from i13c.sem.callsite import CallSiteId
from i13c.sem.flowgraphs import FlowGraph, FlowNode
from i13c.sem.function import Function, FunctionId
from i13c.sem.resolve import Resolution
from i13c.sem.snippet import Snippet, SnippetId


@dataclass(kw_only=True)
class Terminality:
    noreturn: bool


def build_terminalities(
    snippets: Dict[SnippetId, Snippet],
    functions: Dict[FunctionId, Function],
    flowgraphs: Dict[FunctionId, FlowGraph],
    resolutions: Dict[CallSiteId, Resolution],
) -> Dict[FunctionId, Terminality]:

    def is_callable_terminal(callable: Callable) -> bool:
        match callable:
            case Callable(kind=b"snippet", target=SnippetId() as target):
                return snippets[target].noreturn
            case Callable(kind=b"function", target=FunctionId() as target):
                return terminalities[target].noreturn
            case _:
                return False

    def is_callsite_terminal(cid: CallSiteId) -> bool:
        resolution = resolutions[cid]

        if not resolution.accepted:
            return False

        for accepted in resolution.accepted:
            if not is_callable_terminal(accepted.callable):
                return False

        return True

    def has_path_to_exit(flowgraph: FlowGraph) -> bool:
        visited: Set[FlowNode] = set()
        stack: List[FlowNode] = [flowgraph.entry]

        while stack:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            if node == flowgraph.exit:
                return True

            # if callsite is terminal, ignore its successors
            if isinstance(node, CallSiteId):
                if is_callsite_terminal(node):
                    continue

            # pick up successors
            for successor in flowgraph.edges.get(node, []):
                stack.append(successor)

        return False

    terminalities: Dict[FunctionId, Terminality] = {}

    for fid in functions.keys():
        terminalities[fid] = Terminality(noreturn=False)

    changed = True
    while changed:
        changed = False

        for fid in functions.keys():
            if terminalities[fid].noreturn:
                continue

            if not has_path_to_exit(flowgraphs[fid]):
                terminalities[fid] = Terminality(noreturn=True)
                changed = True

    return terminalities
