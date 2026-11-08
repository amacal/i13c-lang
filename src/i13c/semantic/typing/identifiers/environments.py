from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class EnvironmentId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("environment", f"{self.value:<{length}}"))
