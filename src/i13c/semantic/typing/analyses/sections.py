from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class SectiontId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("section", f"{self.value:<{length}}"))


@dataclass(kw_only=True, repr=False)
class Section:
    type: str
    data: bytes
