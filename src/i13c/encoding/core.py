from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.analyses.fnlets import FunctionId
from i13c.semantic.typing.identifiers.asmlets import AsmletId

RelocationTarget = AsmletId | FunctionId | int


@dataclass(kw_only=True)
class RelocationInfo:
    target: RelocationTarget
    width: Kind[1, 4]
    offset: int


class UnreachableEncodingError(Exception):
    pass
