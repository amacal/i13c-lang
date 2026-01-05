from typing import Dict, List, Optional, Set

from i13c.core.mapping import OneToOne
from i13c.sem.infra import Configuration
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

    def is_callsite_terminal(cid: CallSiteId) -> Optional[bool]:
        resolution = resolutions.get(cid)

        # ignore not resolved or ambiguously resolved callsites
        if len(resolution.accepted) != 1:
            return None

        # only one acceptance is expected here
        for accepted in resolution.accepted:
            if not is_callable_terminal(accepted.callable):
                return False

        return True

    def has_path_to_exit(flowgraph: FlowGraph) -> Optional[bool]:
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
                is_terminal = is_callsite_terminal(node)

                # break the search if we cannot determine terminality
                if is_terminal is None:
                    return None

                if is_terminal:
                    continue

            # pick up successors
            for successor in flowgraph.edges.get(node, []):
                stack.append(successor)

        return False

    terminalities: Dict[FunctionId, Terminality] = {}
    ignored: Set[FunctionId] = set()

    for fid in functions.keys():
        terminalities[fid] = Terminality(noreturn=False)

    changed = True
    while changed:
        changed = False

        for fid in functions.keys():
            # don't process already terminal functions
            if terminalities[fid].noreturn:
                continue

            # don't process already ignored functions
            if fid in ignored:
                continue

            flowgraph = flowgraphs.get(fid)
            detected = has_path_to_exit(flowgraph)

            if detected is None:
                ignored.add(fid)

            if detected == False:
                terminalities[fid] = Terminality(noreturn=True)
                changed = True

    # don't expose ignored functions
    for fid in ignored:
        del terminalities[fid]

    return OneToOne[FunctionId, Terminality].instance(terminalities)
