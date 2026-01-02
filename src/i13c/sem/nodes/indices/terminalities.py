from typing import Dict, List, Set

from i13c.sem.infra import Configuration, OneToOne
from i13c.sem.typing.entities.callables import Callable
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import Function, FunctionId
from i13c.sem.typing.entities.snippets import Snippet, SnippetId
from i13c.sem.typing.indices.flowgraphs import FlowGraph, FlowNode
from i13c.sem.typing.indices.terminalities import Terminality
from i13c.sem.typing.resolutions.callsites import CallSiteResolution


def configure_terminality_by_function() -> Configuration:
    return Configuration(
        builder=build_terminalities,
        produces=("indices/terminality-by-function",),
        requires=frozenset(
            {
                ("snippets", "entities/snippets"),
                ("functions", "entities/functions"),
                ("flowgraphs", "indices/flowgraph-by-function"),
                ("resolutions", "resolutions/callsites"),
            }
        ),
    )


def build_terminalities(
    snippets: OneToOne[SnippetId, Snippet],
    functions: OneToOne[FunctionId, Function],
    flowgraphs: OneToOne[FunctionId, FlowGraph],
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
) -> OneToOne[FunctionId, Terminality]:
    def is_callable_terminal(callable: Callable) -> bool:
        match callable:
            case Callable(kind=b"snippet", target=SnippetId() as target):
                return snippets.get(target).noreturn
            case Callable(kind=b"function", target=FunctionId() as target):
                return terminalities[target].noreturn
            case _:
                return False

    def is_callsite_terminal(cid: CallSiteId) -> bool:
        resolution = resolutions.get(cid)

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

            if not has_path_to_exit(flowgraphs.get(fid)):
                terminalities[fid] = Terminality(noreturn=True)
                changed = True

    return OneToOne[FunctionId, Terminality].instance(terminalities)
