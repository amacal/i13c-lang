from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.syntax.source import Span

ReferenceRejectionReason = Kind["unknown-name"]
ReferenceTarget = ParameterAcceptance | LabelAcceptance


@dataclass(kw_only=True)
class ReferenceRejection:
    ref: Span
    id: ReferenceId

    name: bytes
    reason: ReferenceRejectionReason


@dataclass(kw_only=True)
class ReferenceAcceptance:
    ref: Span
    id: ReferenceId

    name: bytes
    target: ReferenceTarget


@dataclass(kw_only=True)
class ReferenceResolution:
    ref: Span
    id: ReferenceId

    accepted: list[ReferenceAcceptance]
    rejected: list[ReferenceRejection]
