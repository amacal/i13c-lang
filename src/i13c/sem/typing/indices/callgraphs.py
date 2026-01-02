from dataclasses import dataclass

from i13c.sem.typing.entities.callables import CallableTarget
from i13c.sem.typing.entities.callsites import CallSiteId


@dataclass(kw_only=True)
class CallPair:
    callsite: CallSiteId
    target: CallableTarget

    @staticmethod
    def instance(callsite: CallSiteId, target: CallableTarget) -> CallPair:
        return CallPair(callsite=callsite, target=target)

    def describe(self) -> str:
        return f"callsite={self.callsite.identify(2)} target={self.target.identify(2)}"
