from dataclasses import dataclass
from typing import Dict, Tuple, Union


@dataclass(kw_only=True)
class EnterFrame:
    size: int


@dataclass(kw_only=True)
class ExitFrame:
    size: int


@dataclass(kw_only=True)
class Preserve:
    registers: Dict[int, int]


@dataclass(kw_only=True)
class Restore:
    registers: Dict[int, int]


Abstracts = Union[
    EnterFrame,
    ExitFrame,
    Preserve,
    Restore,
]


@dataclass(kw_only=True, frozen=True)
class AbstractId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("abstract", f"{self.value:<{length}}"))


AbstractEntry = Tuple[AbstractId, Abstracts]
