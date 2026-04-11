from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.entities.slots import SlotId
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.semantic.typing.resolutions.types import TypeAcceptance
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class SlotRejection:
    ref: Span


@dataclass(kw_only=True)
class SlotAcceptance:
    ref: Span
    id: SlotId

    name: bytes
    bind: BindAcceptance
    type: TypeAcceptance


@dataclass(kw_only=True)
class SlotResolution:
    accepted: List[SlotAcceptance]
    rejected: List[SlotRejection]
