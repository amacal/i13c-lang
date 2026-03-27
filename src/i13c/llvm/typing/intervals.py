from dataclasses import dataclass
from typing import List


@dataclass(kw_only=True)
class RegisterInterval:
    vreg: int
    start: int
    end: int


@dataclass(kw_only=True)
class IntervalPressure:
    index: int
    pressure: int
    registers: List[int]
