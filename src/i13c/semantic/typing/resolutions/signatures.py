from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.syntax.source import Span

SignatureRejectionReason = Kind[
    "duplicated-name",
    "too-many-parameters",
]


@dataclass(kw_only=True)
class SignatureRejection:
    ref: Span
    id: SignatureId
    reason: SignatureRejectionReason


@dataclass(kw_only=True)
class SignatureAcceptance:
    ref: Span
    id: SignatureId

    name: bytes
    parameters: list[ParameterAcceptance]


@dataclass(kw_only=True)
class SignatureResolution:
    ref: Span
    id: SignatureId

    accepted: list[SignatureAcceptance]
    rejected: list[SignatureRejection]
