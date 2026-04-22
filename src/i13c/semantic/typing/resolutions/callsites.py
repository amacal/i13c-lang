from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.syntax.source import Span

CallSiteRejectionReason = Kind[
    "arity-mismatch",
    "type-mismatch",
    "unknown-target",
]

@dataclass(kw_only=True)
class CallSiteRejection:
    ref: Span
    reason: CallSiteRejectionReason


@dataclass(kw_only=True)
class CallSiteAcceptance:
    ref: Span
    id: CallSiteId
    target: SignatureAcceptance


@dataclass(kw_only=True)
class CallSiteResolution:
    accepted: List[CallSiteAcceptance]
    rejected: List[CallSiteRejection]
