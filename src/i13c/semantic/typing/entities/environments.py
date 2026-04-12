from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.labels import LabelId
from i13c.semantic.typing.entities.slots import SlotId
from i13c.syntax.source import Span

EnvironmentKind = Kind["snippet"]
EnvironmentTarget = Union[SlotId, LabelId]


@dataclass(kw_only=True, frozen=True)
class EnvironmentId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("environment", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Environment:
    ref: Span

    kind: EnvironmentKind
    entries: List[EnvironmentTarget]

    def __str__(self) -> str:
        return f"{self.kind}:{len(self.entries)}"
