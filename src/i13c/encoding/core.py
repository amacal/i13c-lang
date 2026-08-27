from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.analyses.asmlets import AsmletId
from i13c.semantic.typing.analyses.fnlets import FunctionId

RelocationTarget = AsmletId | FunctionId | int


@dataclass(kw_only=True)
class RelocationInfo:
    target: RelocationTarget
    width: Kind[1, 4]
    offset: int


class UnreachableEncodingError(Exception):
    pass
