from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.syntax.source import Span

BindingRejectionReason = Kind["duplicated-binds",]
BindingMode = Kind["register", "immediate"]


@dataclass(kw_only=True)
class BindingRejection:
    ref: Span
    owner: SignatureId
    reason: BindingRejectionReason


@dataclass(kw_only=True)
class BindingEntry:
    src: bytes
    dst: bytes
    mode: BindingMode

    def is_immediate(self) -> bool:
        return self.mode == "immediate"


@dataclass(kw_only=True)
class BindingAcceptance:
    ref: Span
    owner: SignatureId
    mapping: list[BindingEntry]


@dataclass(kw_only=True)
class BindingResolution:
    ref: Span
    owner: SignatureId

    accepted: list[BindingAcceptance]
    rejected: list[BindingRejection]
