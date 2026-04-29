from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from i13c.semantic.core import Hex
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.semantic.typing.resolutions.flags import FlagsAcceptance
from i13c.semantic.typing.resolutions.operands import OperandSymbol
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
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

    signature: SignatureId
    keys: Dict[bytes, Hex]

    binding: List[BindAcceptance]
    parameters: List[ParameterAcceptance]
    flags: Optional[FlagsAcceptance]
    instructions: List[AsmletInstruction]
    callsites: List[CallSiteAcceptance]


@dataclass(kw_only=True)
class AsmletInstruction:
    ref: Span
    id: InstructionId

    mnemonic: bytes
    operands: List[AsmletOperand]


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


@dataclass(kw_only=True)
class AsmletOperandAddress:
    base: AsmletOperandRegister
    displacement: Optional[Hex]


AsmletOperandTarget = Union[
    AsmletOperandRegister,
    AsmletOperandImmediate,
    AsmletOperandAddress,
    AsmletOperandRelocation,
]
