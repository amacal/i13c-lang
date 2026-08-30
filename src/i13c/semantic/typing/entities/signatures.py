from dataclasses import dataclass

from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.syntax.source import Span
from i13c.semantic.syntax import NodeId

@dataclass(kw_only=True, frozen=True)
class SignatureId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("signature", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Signature:
    ref: Span
    nid: NodeId

    name: bytes
    parameters: list[ParameterId]
