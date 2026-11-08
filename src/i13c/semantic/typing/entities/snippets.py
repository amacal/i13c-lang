from dataclasses import dataclass

from i13c.semantic.typing.identifiers.flags import FlagsId
from i13c.semantic.typing.identifiers.instructions import InstructionId
from i13c.semantic.typing.identifiers.labels import LabelId
from i13c.semantic.typing.identifiers.signatures import SignatureId
from i13c.syntax.source import Span

InstructionOrLabel = InstructionId | LabelId


@dataclass(kw_only=True)
class Snippet:
    ref: Span
    signature: SignatureId

    flags: FlagsId | None
    body: list[InstructionOrLabel]
