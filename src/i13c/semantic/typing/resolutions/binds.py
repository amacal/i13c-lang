from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.binds import BindId
from i13c.syntax.source import Span

BindRejectionReason = Kind[
    "unknown-register",
    "incorrect-width",
]

BindMode = Kind["register", "immediate"]


@dataclass(kw_only=True)
class BindRejection:
    ref: Span
    reason: BindRejectionReason


@dataclass(kw_only=True)
class BindAcceptance:
    ref: Span
    id: BindId

    target: bytes
    mode: BindMode


@dataclass(kw_only=True)
class BindResolution:
    accepted: List[BindAcceptance]
    rejected: List[BindRejection]
