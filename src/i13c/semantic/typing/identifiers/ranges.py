from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class RangeId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("range", f"{self.value:<{length}}"))
