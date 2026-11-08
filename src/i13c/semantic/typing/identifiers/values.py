from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class ValueId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("value", f"{self.value:<{length}}"))
