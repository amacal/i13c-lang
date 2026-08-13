from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.entities.calls import CallId
from i13c.syntax.source import Span

CallRejectionReason = Kind["unknown"]


@dataclass(kw_only=True)
class CallAcceptance:
    ref: Span
    id: CallId
    target: Calling


@dataclass(kw_only=True)
class CallRejection:
    ref: Span
    id: CallId
    reason: CallRejectionReason


@dataclass(kw_only=True)
class CallResolution:
    ref: Span
    id: CallId

    accepted: list[CallAcceptance]
    rejected: list[CallRejection]
