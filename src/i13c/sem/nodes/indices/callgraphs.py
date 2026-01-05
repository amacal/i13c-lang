from typing import Dict, List, Tuple

from i13c.core.mapping import OneToMany, OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.callables import CallableTarget
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import Function, FunctionId
from i13c.sem.typing.entities.snippets import Snippet, SnippetId
from i13c.sem.typing.indices.callgraphs import CallPair
from i13c.sem.typing.resolutions.callsites import CallSiteResolution


def configure_callgraphs() -> Configuration:
    return Configuration(
        builder=build_callgraphs,
        produces=(
            "indices/calls-by-caller",
            "indices/calls-by-callee",
        ),
        requires=frozenset(
            {
                ("snippets", "entities/snippets"),
                ("functions", "entities/functions"),
                ("resolutions", "resolutions/callsites"),
            }
        ),
    )


def build_callgraphs(
    snippets: OneToOne[SnippetId, Snippet],
    functions: OneToOne[FunctionId, Function],
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
) -> Tuple[OneToMany[CallableTarget, CallPair], OneToMany[CallableTarget, CallPair]]:
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
            for accepted in resolutions.get(statement).accepted:
                callee = accepted.callable.target
                by_caller[fid].append(CallPair.instance(statement, callee))
                by_callee[callee].append(CallPair.instance(statement, fid))

    return (
        OneToMany[CallableTarget, CallPair].instance(by_caller),
        OneToMany[CallableTarget, CallPair].instance(by_callee),
    )
