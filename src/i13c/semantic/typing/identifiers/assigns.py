from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class AssignId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("assign", f"{self.value:<{length}}"))
