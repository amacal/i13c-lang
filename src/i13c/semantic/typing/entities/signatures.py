from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.entities.slots import SlotId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class SignatureId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("signature", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Signature:
    ref: Span
    name: bytes

    slots: List[SlotId]

    def __str__(self) -> str:
        return f"{self.name.decode()}:{len(self.slots)}"
