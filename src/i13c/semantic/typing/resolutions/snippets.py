from dataclasses import dataclass
from typing import List, Optional

from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.bindings import BindingAcceptance
from i13c.semantic.typing.resolutions.flags import FlagsAcceptance
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
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
    flags: Optional[FlagsAcceptance]
    instructions: List[InstructionAcceptance]


@dataclass(kw_only=True)
class SnippetResolution:
    accepted: List[SnippetAcceptance]
    rejected: List[SnippetRejection]
