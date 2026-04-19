from dataclasses import dataclass

from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class BindId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("bind", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Bind:
    ref: Span
    ctx: ParameterId

    src: bytes
    dst: bytes

    def __str__(self) -> str:
        return f"{self.src.decode()}:{self.dst.decode()}"
