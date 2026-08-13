from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.syntax.source import Span

BindingRejectionReason = Kind["duplicated-binds",]


@dataclass(kw_only=True)
class BindingRejection:
    ref: Span
    owner: SignatureId
    reason: BindingRejectionReason


@dataclass(kw_only=True)
class BindingAcceptance:
    ref: Span
    owner: SignatureId
    binds: list[BindAcceptance]


@dataclass(kw_only=True)
class BindingResolution:
    ref: Span
    owner: SignatureId

    accepted: list[BindingAcceptance]
    rejected: list[BindingRejection]
