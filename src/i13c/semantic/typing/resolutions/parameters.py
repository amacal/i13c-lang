from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.resolutions.types import TypeAcceptance
from i13c.syntax.source import Span

ParameterBind = Kind["literal", "value"]


@dataclass(kw_only=True)
class ParameterRejection:
    ref: Span
    id: ParameterId


@dataclass(kw_only=True)
class ParameterAcceptance:
    ref: Span
    id: ParameterId

    name: bytes
    type: TypeAcceptance
    bind: ParameterBind

    def __str__(self) -> str:
        return f"{self.bind}({self.name.decode()}:{self.type})"


@dataclass(kw_only=True)
class ParameterResolution:
    ref: Span
    id: ParameterId

    accepted: list[ParameterAcceptance]
    rejected: list[ParameterRejection]
