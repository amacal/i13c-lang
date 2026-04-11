from dataclasses import dataclass

from i13c.semantic.typing.entities.binds import BindId
from i13c.semantic.typing.entities.types import TypeId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class SlotId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("slot", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Slot:
    ref: Span
    name: bytes

    bind: BindId
    type: TypeId

    def __str__(self) -> str:
        return f"{self.name.decode()}, {self.bind.identify(1)}, {self.type.identify(1)}"
