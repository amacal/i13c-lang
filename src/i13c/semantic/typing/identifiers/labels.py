from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class LabelId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("label", f"{self.value:<{length}}"))
