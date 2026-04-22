from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.resolutions.cflows import ControlFlowEntry
from i13c.syntax.source import Span

ExpressionRejectionReason = Kind["unresolved"]


@dataclass(kw_only=True)
class ExpressionAcceptance:
    ref: Span
    id: ExpressionId

    name: bytes
    environment: ControlFlowEntry


@dataclass(kw_only=True)
class ExpressionRejection:
    ref: Span
    reason: ExpressionRejectionReason


@dataclass(kw_only=True)
class ExpressionResolution:
    accepted: List[ExpressionAcceptance]
    rejected: List[ExpressionRejection]
