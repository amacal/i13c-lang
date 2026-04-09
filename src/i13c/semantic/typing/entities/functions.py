from dataclasses import dataclass
from typing import List, Union

from i13c.semantic.core import Identifier
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.parameters import ParameterId
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
    identifier: Identifier
    noreturn: bool
    parameters: List[ParameterId]
    statements: List[Statement]

    def signature(self) -> str:
        parameters = ", ".join([parameter.identify(2) for parameter in self.parameters])
        return f"{self.identifier.data.decode()}/{len(self.parameters)} ({parameters})"
