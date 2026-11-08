from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class CallId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("call", f"{self.value:<{length}}"))
