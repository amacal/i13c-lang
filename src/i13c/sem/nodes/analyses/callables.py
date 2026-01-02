from typing import List, Set

from i13c.sem.infra import Configuration, OneToMany, OneToOne
from i13c.sem.typing.entities.callables import CallableTarget
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.indices.callgraphs import CallPair
from i13c.sem.typing.indices.entrypoints import EntryPoint


def configure_callables_live() -> Configuration:
    return Configuration(
        builder=build_callable_live,
        produces=("analyses/callables/live",),
        requires=frozenset(
            {
                ("entrypoints", "indices/entrypoints-by-callable"),
                ("callgraph_live", "analyses/calls-by-caller/live"),
            }
        ),
    )


def build_callable_live(
    entrypoints: OneToOne[CallableTarget, EntryPoint],
    callgraph_live: OneToMany[CallableTarget, CallPair],
) -> Set[CallableTarget]:
    out: Set[CallableTarget] = set()
    stack: List[CallableTarget] = []

    # entrypoints are live
    for entrypoint in entrypoints.values():
        out.add(entrypoint.target)
        stack.append(entrypoint.target)

    # propagate liveness through callgraph
    # by attaching only live functions

    while stack:
        for pair in callgraph_live.find(stack.pop()):
            if isinstance(pair.target, FunctionId):
                if pair.target not in out:
                    stack.append(pair.target)
                    out.add(pair.target)
    return out
