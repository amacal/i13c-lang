from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class VariableId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("variable", f"{self.value:<{length}}"))
