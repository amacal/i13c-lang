from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.syntax.source import Span

FlagsRejectionReason = Kind["duplicated-register",]


@dataclass(kw_only=True)
class FlagsRejection:
    ref: Span
    reason: FlagsRejectionReason


@dataclass(kw_only=True)
class FlagsAcceptance:
    ref: Span
    id: FlagsId

    noreturn: bool
    clobbers: List[RegisterAcceptance]


@dataclass(kw_only=True)
class FlagsResolution:
    accepted: List[FlagsAcceptance]
    rejected: List[FlagsRejection]
