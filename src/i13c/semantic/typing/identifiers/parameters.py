from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class ParameterId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("parameter", f"{self.value:<{length}}"))
