from dataclasses import dataclass
from typing import Literal as Kind

from i13c.semantic.typing.entities.callsites import CallSite
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.identifiers.callsites import CallSiteId
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.results import ResultAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from i13c.syntax.source import Span

CallSiteRejectionReason = Kind[
    "arity-mismatch",
    "type-mismatch",
    "unknown-target",
    "ambiguous-target",
    "too-many-arguments",
    "not-literal",
]

# the output of a callsite cannot be comparable
# it has to be comparable by the reference (ref)


@dataclass(kw_only=True, eq=False)
class CallSiteOutput:
    target: ResultAcceptance

    def __str__(self) -> str:
        return str(self.target)


@dataclass(kw_only=True)
class CallSiteRejection:
    ref: Span
    id: CallSiteId
    target: CallSite
    reason: CallSiteRejectionReason


@dataclass(kw_only=True, repr=False)
class CallSiteAcceptance:
    ref: Span
    id: CallSiteId

    sig: SignatureId
    stmt: StatementId

    signature: SignatureAcceptance
    arguments: list[CallSiteArgument]
    output: CallSiteOutput | None


CallSiteArgument = (
    LiteralAcceptance | ParameterAcceptance | ValueAcceptance | CallSiteAcceptance
)


@dataclass(kw_only=True)
class CallSiteResolution:
    ref: Span
    id: CallSiteId

    accepted: list[CallSiteAcceptance]
    rejected: list[CallSiteRejection]
