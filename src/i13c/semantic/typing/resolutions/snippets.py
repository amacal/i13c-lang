from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.bindings import BindingAcceptance
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.syntax.source import Span


@dataclass(kw_only=True)
class SnippetRejection:
    ref: Span
    id: SnippetId


@dataclass(kw_only=True)
class SnippetAcceptance:
    ref: Span
    id: SnippetId

    binding: BindingAcceptance
    signature: SignatureAcceptance
    instructions: List[InstructionAcceptance]

    noreturn: bool
    clobbers: List[RegisterAcceptance]


@dataclass(kw_only=True)
class SnippetResolution:
    ref: Span
    id: SnippetId

    accepted: List[SnippetAcceptance]
    rejected: List[SnippetRejection]
