from dataclasses import dataclass
from typing import List

from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class LiteralRejection:
    ref: Span


@dataclass(kw_only=True)
class LiteralAcceptance:
    ref: Span
    id: LiteralId
    target: Hex


@dataclass(kw_only=True)
class LiteralResolution:
    accepted: List[LiteralAcceptance]
    rejected: List[LiteralRejection]
