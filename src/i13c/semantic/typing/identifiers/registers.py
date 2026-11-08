from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class RegisterId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("register", f"{self.value:<{length}}"))
