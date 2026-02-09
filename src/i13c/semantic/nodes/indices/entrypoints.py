from typing import Dict

from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.callables import CallableTarget
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.indices.entrypoints import EntryPoint, EntryPointName


def configure_entrypoint_by_callable() -> GraphNode:
    return GraphNode(
        builder=build_entrypoints,
        produces=("indices/entrypoints-by-callable",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("snippets", "entities/snippets"),
            }
        ),
    )


def build_entrypoints(
    functions: OneToOne[FunctionId, Function],
    snippets: OneToOne[SnippetId, Snippet],
) -> OneToOne[CallableTarget, EntryPoint]:

    out: Dict[CallableTarget, EntryPoint] = {}

    for fid, function in functions.items():
        if function.identifier.name == EntryPointName:
            if function.noreturn and not function.parameters:
                out[fid] = EntryPoint(kind=b"function", target=fid)

    return OneToOne[CallableTarget, EntryPoint].instance(out)
