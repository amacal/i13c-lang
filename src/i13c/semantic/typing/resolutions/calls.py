from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.calls import CallId
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.syntax.source import Span

CallRejectionReason = Kind["unknown"]


@dataclass(kw_only=True)
class CallAcceptance:
    ref: Span
    id: CallId

    target: CallSiteAcceptance


@dataclass(kw_only=True)
class CallRejection:
    reason: CallRejectionReason


@dataclass(kw_only=True)
class CallResolution:
    accepted: List[CallAcceptance]
    rejected: List[CallRejection]
