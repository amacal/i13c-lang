from dataclasses import dataclass

from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class MnemonicId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("mnemonic", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Mnemonic:
    ref: Span
    name: bytes

    def __str__(self) -> str:
        return self.name.decode()
