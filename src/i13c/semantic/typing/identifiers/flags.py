from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class FlagsId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("flags", f"{self.value:<{length}}"))
