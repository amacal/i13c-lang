from dataclasses import dataclass

from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.syntax.source import Span


@dataclass(kw_only=True, frozen=True)
class CallId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("call", f"{self.value:<{length}}"))



@dataclass(kw_only=True)
class Call:
    ref: Span
    target: CallSiteId
