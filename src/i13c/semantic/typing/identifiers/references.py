from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class ReferenceId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("reference", f"{self.value:<{length}}"))
