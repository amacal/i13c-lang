from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.syntax.source import Span

SignatureRejectionReason = Kind[
    "duplicated-name",
]


@dataclass(kw_only=True)
class SignatureRejection:
    ref: Span
    reason: SignatureRejectionReason


@dataclass(kw_only=True)
class SignatureAcceptance:
    ref: Span
    id: SignatureId

    name: bytes
    parameters: List[ParameterAcceptance]


@dataclass(kw_only=True)
class SignatureResolution:
    accepted: List[SignatureAcceptance]
    rejected: List[SignatureRejection]
