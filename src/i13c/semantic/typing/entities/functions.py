from dataclasses import dataclass
from typing import List, Optional, Union

from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.values import ValueId
from i13c.syntax.source import Span

Statement = Union[CallSiteId, ValueId]


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("function", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Function:
    ref: Span
    signature: SignatureId
    flags: Optional[FlagsId]
    statements: List[Statement]
