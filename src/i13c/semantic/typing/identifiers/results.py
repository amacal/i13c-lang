from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class ResultId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("result", f"{self.value:<{length}}"))
