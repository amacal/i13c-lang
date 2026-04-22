from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.entities.parameters import ParameterId
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
    parameters: List[ParameterId]
