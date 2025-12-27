from dataclasses import dataclass
from typing import Dict, List
from typing import Literal as Kind
from typing import Union

from i13c.sem.function import Function, FunctionId
from i13c.sem.snippet import Snippet, SnippetId
from i13c.sem.terminal import Terminality

EntryPointName: bytes = b"main"

EntryPointKind = Kind[
    b"function",
    b"snippet",
]


@dataclass
class EntryPoint:
    kind: EntryPointKind
    target: Union[FunctionId, SnippetId]


def build_entrypoints(
    functions: Dict[FunctionId, Function],
    snippets: Dict[SnippetId, Snippet],
    terminalities: Dict[FunctionId, Terminality],
) -> List[EntryPoint]:

    out: List[EntryPoint] = []

    for fid, function in functions.items():
        if function.identifier.name == EntryPointName:
            if terminalities[fid].noreturn:
                out.append(EntryPoint(kind=b"function", target=fid))

    for sid, snippet in snippets.items():
        if snippet.identifier.name == EntryPointName:
            if snippet.noreturn:
                out.append(EntryPoint(kind=b"snippet", target=sid))

    return out
