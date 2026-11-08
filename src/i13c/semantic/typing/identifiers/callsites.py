from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class CallSiteId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("callsite", f"{self.value:<{length}}"))
