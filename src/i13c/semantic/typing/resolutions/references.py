from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.slots import SlotAcceptance
from i13c.syntax.source import Span

ReferenceRejectionReason = Kind["unknown-name"]
ReferenceTarget = Union[SlotAcceptance, LabelAcceptance]


@dataclass(kw_only=True)
class ReferenceRejection:
    ref: Span
    name: bytes
    reason: ReferenceRejectionReason


@dataclass(kw_only=True)
class ReferenceAcceptance:
    ref: Span
    id: ReferenceId

    name: bytes
    target: ReferenceTarget


@dataclass(kw_only=True)
class ReferenceResolution:
    accepted: List[ReferenceAcceptance]
    rejected: List[ReferenceRejection]
