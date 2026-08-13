from dataclasses import dataclass


@dataclass(kw_only=True)
class RegisterInterval:
    vreg: int
    start: int
    end: int


@dataclass(kw_only=True)
class IntervalPressure:
    index: int
    pressure: int
    registers: list[int]
