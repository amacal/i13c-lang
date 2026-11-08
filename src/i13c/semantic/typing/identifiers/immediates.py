from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class ImmediateId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("immediate", f"{self.value:<{length}}"))
