from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class LiteralId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("literal", f"{self.value:<{length}}"))
