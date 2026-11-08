from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class DisplacementId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("displacement", f"{self.value:<{length}}"))
