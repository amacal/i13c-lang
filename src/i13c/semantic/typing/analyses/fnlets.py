from dataclasses import dataclass

from i13c.semantic.typing.analyses import llvm
from i13c.semantic.typing.analyses.statements import StatementInstruction
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.syntax.source import Span

FnletInstruction = (
    StatementInstruction
    | llvm.PUSH
    | llvm.POP
    | llvm.ADD
    | llvm.SUB
    | llvm.EPILOG
    | llvm.PROLOG
    | llvm.JMP
)


@dataclass(kw_only=True, repr=False)
class FnletBlock:
    instructions: list[FnletInstruction]


@dataclass(kw_only=True, repr=False)
class Fnlet:
    ref: Span
    target: FunctionId

    blocks: list[FnletBlock]
    signature: SignatureAcceptance
