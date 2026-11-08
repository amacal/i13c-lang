from dataclasses import dataclass


@dataclass(kw_only=True, repr=False)
class Section:
    type: str
    data: bytes
