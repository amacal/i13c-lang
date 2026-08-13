from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(kw_only=True)
class StackFrame:
    size: int
    regs: dict[int, int]

    def slot_at_register(self, reg: int) -> int | None:
        return self.regs.get(reg)

    def registers_at_slot(self, idx: int) -> Iterable[int]:
        return (reg for reg, slot in self.regs.items() if slot == idx)
