from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class UsageId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("usage", f"{self.value:<{length}}"))
