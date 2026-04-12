from dataclasses import dataclass
from typing import Dict, List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.environments import EnvironmentId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.slots import SlotAcceptance
from i13c.syntax.source import Span

EnvironmentKind = Kind["snippet"]
EnvironmentTarget = Union[SlotAcceptance, LabelAcceptance]
EnvironmentRejectionReason = Kind["duplicated-name"]


@dataclass(kw_only=True)
class EnvironmentRejection:
    ref: Span
    reason: EnvironmentRejectionReason


@dataclass(kw_only=True)
class EnvironmentAcceptance:
    ref: Span
    id: EnvironmentId

    ctx: SnippetId
    kind: EnvironmentKind
    entries: Dict[bytes, EnvironmentTarget]


@dataclass(kw_only=True)
class EnvironmentResolution:
    accepted: List[EnvironmentAcceptance]
    rejected: List[EnvironmentRejection]
