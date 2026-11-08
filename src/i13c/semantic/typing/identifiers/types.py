from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class TypeId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("type", f"{self.value:<{length}}"))
