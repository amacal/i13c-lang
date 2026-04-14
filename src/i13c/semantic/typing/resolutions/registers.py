from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.registers import RegisterId
from i13c.syntax.source import Span

RegisterRejectionReason = Kind[
    "unknown-register",
]

RegisterWidth = Kind[8, 16, 32, 64]
RegisterKind = Kind["low", "high", "8bit", "16bit", "32bit", "64bit", "rip"]


@dataclass(kw_only=True)
class RegisterRejection:
    ref: Span
    reason: RegisterRejectionReason


@dataclass(kw_only=True)
class RegisterAcceptance:
    ref: Span
    id: RegisterId

    name: bytes
    kind: RegisterKind
    width: RegisterWidth


@dataclass(kw_only=True)
class RegisterResolution:
    accepted: List[RegisterAcceptance]
    rejected: List[RegisterRejection]
