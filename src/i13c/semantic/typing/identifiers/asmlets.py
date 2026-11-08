from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class AsmletId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("asmlet", f"{self.value:<{length}}"))

    def __str__(self) -> str:
        return self.identify(1)
