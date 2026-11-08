from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class IndexId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("index", f"{self.value:<{length}}"))
