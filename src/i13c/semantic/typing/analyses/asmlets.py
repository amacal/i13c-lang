from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.operands import OperandSymbol, RegisterAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class AsmletId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("asmlet", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Asmlet:
    ref: Span
    id: AsmletId

    name: bytes
    source: SnippetId

    signature: SignatureAcceptance
    keys: dict[bytes, Hex]

    bindings: list[BindAcceptance]
    parameters: list[ParameterAcceptance]

    noreturn: bool
    clobbers: list[RegisterAcceptance]

    instructions: list[AsmletInstruction]
    callsites: list[CallSiteAcceptance]


@dataclass(kw_only=True)
class AsmletInstruction:
    ref: Span
    id: InstructionId

    mnemonic: bytes
    operands: list[AsmletOperand]


@dataclass(kw_only=True)
class AsmletOperand:
    ref: Span
    target: AsmletOperandTarget
    symbol: OperandSymbol


@dataclass(kw_only=True)
class AsmletOperandRegister:
    name: bytes


@dataclass(kw_only=True)
class AsmletOperandImmediate:
    value: Hex


@dataclass(kw_only=True)
class AsmletOperandRelocation:
    offset: int


AsmletDisplacementOffset = bytes
AsmletDisplacementWidth = Kind[0, 8, 32]
AsmletDisplacementDirection = Kind["forward", "backward"]


@dataclass(kw_only=True)
class AsmletOperandIndex:
    scale: Kind[1, 2, 4, 8]
    reg: AsmletOperandRegister

    def __str__(self) -> str:
        return f"{self.scale} * {self.reg}"


@dataclass(kw_only=True)
class AsmletOperandDisplacement:
    width: AsmletDisplacementWidth
    offset: AsmletDisplacementOffset
    direction: AsmletDisplacementDirection

    def __str__(self) -> str:
        if self.direction == "forward":
            return f"+ 0x{self.offset.hex()}"
        else:
            return f"- 0x{self.offset.hex()}"


@dataclass(kw_only=True)
class AsmletOperandAddress:
    base: AsmletOperandRegister | None
    indx: AsmletOperandIndex | None
    disp: AsmletOperandDisplacement | None


AsmletOperandTarget = (
    AsmletOperandRegister
    | AsmletOperandImmediate
    | AsmletOperandAddress
    | AsmletOperandRelocation
)
