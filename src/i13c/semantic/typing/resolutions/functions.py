from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.functions import FunctionId
from i13c.syntax.source import Span

FunctionRejectionReason = Kind["invalid-noreturn"]


@dataclass(kw_only=True)
class FunctionRejection:
    ref: Span
    reason: FunctionRejectionReason


@dataclass(kw_only=True)
class FunctionAcceptance:
    ref: Span
    id: FunctionId



@dataclass(kw_only=True)
class FunctionResolution:
    accepted: List[FunctionAcceptance]
    rejected: List[FunctionRejection]
