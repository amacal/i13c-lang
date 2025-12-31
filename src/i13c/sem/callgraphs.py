from typing import Dict, List, Tuple

from i13c.sem.callable import CallableTarget
from i13c.sem.callsite import CallSiteId
from i13c.sem.function import Function, FunctionId
from i13c.sem.resolve import Resolution
from i13c.sem.snippet import Snippet, SnippetId

CallPair = Tuple[CallSiteId, CallableTarget]


def build_callgraph(
    snippets: Dict[SnippetId, Snippet],
    functions: Dict[FunctionId, Function],
    resolutions: Dict[CallSiteId, Resolution],
) -> Tuple[Dict[CallableTarget, List[CallPair]], Dict[CallableTarget, List[CallPair]]]:
    by_caller: Dict[CallableTarget, List[CallPair]] = {}
    by_callee: Dict[CallableTarget, List[CallPair]] = {}

    for snid in snippets.keys():
        by_caller[snid] = []
        by_callee[snid] = []

    for fid in functions.keys():
        by_caller[fid] = []
        by_callee[fid] = []

    for fid, function in functions.items():
        for statement in function.statements:
            for accepted in resolutions[statement].accepted:
                callee = accepted.callable.target
                by_caller[fid].append((statement, callee))
                by_callee[callee].append((statement, fid))

    return by_caller, by_callee
