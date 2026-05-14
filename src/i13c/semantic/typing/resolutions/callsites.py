from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance
from i13c.syntax.source import Span

CallSiteRejectionReason = Kind[
    "arity-mismatch",
    "type-mismatch",
    "unknown-target",
]

CallSiteArgument = Union[
    LiteralAcceptance,
    ParameterAcceptance,
    ValueAcceptance,
]


@dataclass(kw_only=True)
class CallSiteRejection:
    ref: Span
    reason: CallSiteRejectionReason


@dataclass(kw_only=True)
class CallSiteAcceptance:
    ref: Span
    id: CallSiteId

    sig: SignatureId
    stmt: StatementId

    signature: SignatureAcceptance
    arguments: List[CallSiteArgument]


@dataclass(kw_only=True)
class CallSiteResolution:
    accepted: List[CallSiteAcceptance]
    rejected: List[CallSiteRejection]
