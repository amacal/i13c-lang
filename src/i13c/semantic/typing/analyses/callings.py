from dataclasses import dataclass

from i13c.semantic.typing.analyses.asmlets import Asmlet
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.resolutions.callsites import (
    CallSiteAcceptance,
    CallSiteArgument,
)
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.syntax.source import Span

CallingTarget = Asmlet | CallSiteAcceptance


@dataclass(kw_only=True)
class CallingBinding:
    idx: int
    register: bytes


@dataclass(kw_only=True)
class Calling:
    ref: Span
    callsite: CallSiteId

    target: CallingTarget
    signature: SignatureAcceptance
    arguments: list[CallSiteArgument]
    parameters: list[ParameterAcceptance]
