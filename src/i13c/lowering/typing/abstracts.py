from dataclasses import dataclass
from typing import Dict, Tuple, Union


@dataclass(kw_only=True)
class EnterFrame:
    size: int

    def native(self) -> str:
        return f"enter {self.size:#010x}"


@dataclass(kw_only=True)
class ExitFrame:
    size: int

    def native(self) -> str:
        return f"exit {self.size:#010x}"


@dataclass(kw_only=True)
class Preserve:
    registers: Dict[int, int]

    def native(self) -> str:
        regs = ", ".join(f"{k}:{v}" for k, v in self.registers.items())
        return f"preserve {regs}"


@dataclass(kw_only=True)
class Restore:
    registers: Dict[int, int]

    def native(self) -> str:
        regs = ", ".join(f"{k}:{v}" for k, v in self.registers.items())
        return f"restore {regs}"


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
