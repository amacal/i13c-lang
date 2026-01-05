from typing import Dict

from i13c.core.mapping import OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.callables import CallableTarget
from i13c.sem.typing.entities.functions import Function, FunctionId
from i13c.sem.typing.entities.snippets import Snippet, SnippetId
from i13c.sem.typing.indices.entrypoints import EntryPoint, EntryPointName
from i13c.sem.typing.indices.terminalities import Terminality


def configure_entrypoint_by_callable() -> Configuration:
    return Configuration(
        builder=build_entrypoints,
        produces=("indices/entrypoints-by-callable",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("snippets", "entities/snippets"),
                ("terminalities", "indices/terminality-by-function"),
            }
        ),
    )


def build_entrypoints(
    functions: OneToOne[FunctionId, Function],
    snippets: OneToOne[SnippetId, Snippet],
    terminalities: OneToOne[FunctionId, Terminality],
) -> OneToOne[CallableTarget, EntryPoint]:

    out: Dict[CallableTarget, EntryPoint] = {}

    for fid, function in functions.items():
        if function.identifier.name == EntryPointName:
            if not function.parameters:
                if terminality := terminalities.find(fid):
                    if terminality.noreturn:
                        out[fid] = EntryPoint(kind=b"function", target=fid)

    for sid, snippet in snippets.items():
        if snippet.identifier.name == EntryPointName:
            if snippet.noreturn and not snippet.slots:
                out[sid] = EntryPoint(kind=b"snippet", target=sid)

    return OneToOne[CallableTarget, EntryPoint].instance(out)
