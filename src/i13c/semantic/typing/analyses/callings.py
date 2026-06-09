from dataclasses import dataclass
from typing import List

from i13c.semantic.typing.analyses.asmlets import Asmlet
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class CallingId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("calling", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class CallingBinding:
    idx: int
    register: bytes


@dataclass(kw_only=True)
class Calling:
    ref: Span
    id: CallingId

    target: Asmlet
    bindings: List[CallingBinding]
    callsites: List[CallSiteAcceptance]
