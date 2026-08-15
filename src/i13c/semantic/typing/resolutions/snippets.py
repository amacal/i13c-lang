from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.bindings import BindingAcceptance
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.syntax.source import Span

SnippetRejectionReason = Kind[
    "unallowed-clobber",
]

@dataclass(kw_only=True)
class SnippetRejection:
    ref: Span
    id: SnippetId

    reason: SnippetRejectionReason


@dataclass(kw_only=True)
class SnippetAcceptance:
    ref: Span
    id: SnippetId

    binding: BindingAcceptance
    signature: SignatureAcceptance
    instructions: list[InstructionAcceptance]

    noreturn: bool
    clobbers: list[RegisterAcceptance]


@dataclass(kw_only=True)
class SnippetResolution:
    ref: Span
    id: SnippetId

    accepted: list[SnippetAcceptance]
    rejected: list[SnippetRejection]
