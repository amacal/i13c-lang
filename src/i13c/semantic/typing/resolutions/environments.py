from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.environments import EnvironmentId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.syntax.source import Span

EnvironmentKind = Kind["snippet"]
EnvironmentTarget = ParameterAcceptance | LabelAcceptance
EnvironmentRejectionReason = Kind["duplicated-name"]


@dataclass(kw_only=True)
class EnvironmentRejection:
    ref: Span
    id: EnvironmentId
    reason: EnvironmentRejectionReason


@dataclass(kw_only=True)
class EnvironmentAcceptance:
    ref: Span
    id: EnvironmentId

    ctx: SnippetId
    kind: EnvironmentKind
    entries: dict[bytes, EnvironmentTarget]


@dataclass(kw_only=True)
class EnvironmentResolution:
    ref: Span
    id: EnvironmentId

    accepted: list[EnvironmentAcceptance]
    rejected: list[EnvironmentRejection]
