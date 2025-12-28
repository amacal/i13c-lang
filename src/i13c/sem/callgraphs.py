from typing import Dict, List, Tuple

from i13c.sem.callable import CallableTarget
from i13c.sem.callsite import CallSiteId
from i13c.sem.function import Function, FunctionId
from i13c.sem.resolve import Resolution
from i13c.sem.snippet import Snippet, SnippetId

CallPair = Tuple[CallSiteId, CallableTarget]
CallGraphs = Dict[CallableTarget, List[CallPair]]


def build_callgraph(
    snippets: Dict[SnippetId, Snippet],
    functions: Dict[FunctionId, Function],
    resolutions: Dict[CallSiteId, Resolution],
) -> CallGraphs:
    out: CallGraphs = {}

    for snid in snippets.keys():
        out[snid] = []

    for fid in functions.keys():
        out[fid] = []

    for fid, function in functions.items():
        for statement in function.statements:
            for accepted in resolutions[statement].accepted:
                out[fid].append((statement, accepted.callable.target))

    return out
