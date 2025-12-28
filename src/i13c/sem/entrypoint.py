from dataclasses import dataclass
from typing import Dict, List

from i13c.sem.callable import CallableKind, CallableTarget
from i13c.sem.function import Function, FunctionId
from i13c.sem.snippet import Snippet, SnippetId

EntryPointName: bytes = b"main"


@dataclass
class EntryPoint:
    kind: CallableKind
    target: CallableTarget


def build_entrypoints(
    functions: Dict[FunctionId, Function],
    snippets: Dict[SnippetId, Snippet],
) -> List[EntryPoint]:

    out: List[EntryPoint] = []

    for fid, function in functions.items():
        if function.identifier.name == EntryPointName:
            if not function.parameters:
                out.append(EntryPoint(kind=b"function", target=fid))

    for sid, snippet in snippets.items():
        if snippet.identifier.name == EntryPointName:
            if snippet.noreturn and not snippet.slots:
                out.append(EntryPoint(kind=b"snippet", target=sid))

    return out
