from dataclasses import dataclass
from typing import List, Union

from i13c.sem.core import Identifier, Type
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.src import Span

Statement = Union[CallSiteId]


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("function", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Parameter:
    name: Identifier
    type: Type

    def signature(self) -> str:
        return f"{self.name}:{self.type}"


@dataclass(kw_only=True)
class Function:
    ref: Span
    identifier: Identifier
    noreturn: bool
    parameters: List[Parameter]
    statements: List[Statement]

    def signature(self) -> str:
        parameters = ", ".join([parameter.signature() for parameter in self.parameters])
        return f"{self.identifier.name.decode()}/{len(self.parameters)} ({parameters})"

    def describe(self) -> str:
        return f"name={self.identifier.name.decode()}/{len(self.parameters)}"
