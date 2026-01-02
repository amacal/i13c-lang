from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.sem.typing.entities.operands import Immediate, Register


@dataclass(kw_only=True)
class OperandRejection:
    pass


OperandAcceptanceKind = Kind[b"register", b"immediate"]
OperandAcceptanceTarget = Union[Register, Immediate]


@dataclass(kw_only=True)
class OperandAcceptance:
    kind: OperandAcceptanceKind
    target: OperandAcceptanceTarget

    def describe(self) -> str:
        return f"kind={self.kind} target={self.target}"


@dataclass(kw_only=True)
class OperandResolution:
    accepted: List[OperandAcceptance]
    rejected: List[OperandRejection]

    def describe(self) -> str:
        candidate = ""

        if len(self.accepted) > 0:
            candidate = self.accepted[0].describe()

        return (
            f"accepted={len(self.accepted)} rejected={len(self.rejected)} {candidate}"
        )
