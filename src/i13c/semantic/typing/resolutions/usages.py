from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.identifiers.usages import UsageId
from i13c.semantic.typing.resolutions.cflows import ControlFlowEntry, ControlFlowTarget
from i13c.syntax.source import Span

UsageRejectionReason = Kind["unresolved"]


@dataclass(kw_only=True)
class UsageAcceptance:
    ref: Span
    id: UsageId

    name: bytes
    target: ControlFlowTarget
    environment: ControlFlowEntry


@dataclass(kw_only=True)
class UsageRejection:
    ref: Span
    id: UsageId

    name: bytes
    reason: UsageRejectionReason


@dataclass(kw_only=True)
class UsageResolution:
    ref: Span
    id: UsageId

    accepted: list[UsageAcceptance]
    rejected: list[UsageRejection]
