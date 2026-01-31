from dataclasses import dataclass
from typing import Dict, Union


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
