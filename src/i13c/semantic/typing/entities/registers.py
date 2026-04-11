from dataclasses import dataclass

from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class RegisterId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("register", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Register:
    ref: Span
    name: bytes

    def __str__(self) -> str:
        return f"{self.name.decode()}"
