from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class ExpressionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("expression", f"{self.value:<{length}}"))
