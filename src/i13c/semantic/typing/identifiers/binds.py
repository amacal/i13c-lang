from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class BindId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("bind", f"{self.value:<{length}}"))
