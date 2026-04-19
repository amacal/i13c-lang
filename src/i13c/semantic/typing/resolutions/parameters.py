from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.resolutions.types import TypeAcceptance
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class ParameterRejection:
    ref: Span


@dataclass(kw_only=True)
class ParameterAcceptance:
    ref: Span
    id: ParameterId

    name: bytes
    type: TypeAcceptance


@dataclass(kw_only=True)
class ParameterResolution:
    accepted: List[ParameterAcceptance]
    rejected: List[ParameterRejection]
