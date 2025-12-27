from dataclasses import dataclass
from typing import Literal as Kind
from typing import Union

from i13c.sem.function import FunctionId
from i13c.sem.snippet import SnippetId

CallableKind = Kind[b"snippet", b"function"]


@dataclass(kw_only=True)
class Callable:
    kind: CallableKind
    target: Union[SnippetId, FunctionId]
