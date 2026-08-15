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
CallingArgument = CallSiteArgument

@dataclass(kw_only=True)
class CallingBinding:
    name: bytes


@dataclass(kw_only=True, eq=False)
class CallingClobber:
    name: bytes


@dataclass(kw_only=True)
class CallingUnbound:
    name: bytes


@dataclass(kw_only=True)
class Calling:
    ref: Span
    callsite: CallSiteId

    target: CallingTarget
    signature: SignatureAcceptance
    arguments: list[CallingArgument]
    parameters: list[ParameterAcceptance]

    bindings: list[CallingBinding]
    clobbers: list[CallingClobber]
    unbounds: list[CallingUnbound]
