from dataclasses import dataclass

from i13c.syntax.source import Span


@dataclass(kw_only=True)
class Mnemonic:
    ref: Span
    name: bytes

    def __str__(self) -> str:
        return self.name.decode()
