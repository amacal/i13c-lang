from dataclasses import dataclass
from typing import List, Optional

from i13c.semantic.syntax import NodeId
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int

    @staticmethod
    def from_context(nid: NodeId) -> FunctionId:
        return FunctionId(value=nid.value)

    def identify(self, length: int) -> str:
        return "#".join(("function", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Function:
    ref: Span
    signature: SignatureId
    flags: Optional[FlagsId]
    statements: List[StatementId]
