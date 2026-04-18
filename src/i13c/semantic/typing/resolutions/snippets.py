from dataclasses import dataclass
from typing import List
from typing import Literal as Kind

from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.instructions import InstructionAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.syntax.source import Span

SnippetRejectionReason = Kind["duplicated-binds",]


@dataclass(kw_only=True)
class SnippetRejection:
    ref: Span
    reason: SnippetRejectionReason


@dataclass(kw_only=True)
class SnippetAcceptance:
    ref: Span
    id: SnippetId

    signature: SignatureAcceptance
    instructions: List[InstructionAcceptance]


@dataclass(kw_only=True)
class SnippetResolution:
    accepted: List[SnippetAcceptance]
    rejected: List[SnippetRejection]
