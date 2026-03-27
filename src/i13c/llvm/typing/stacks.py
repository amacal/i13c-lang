from dataclasses import dataclass
from typing import Dict, Iterable, Optional


@dataclass(kw_only=True)
class StackFrame:
    size: int
    regs: Dict[int, int]

    def slot_at_register(self, reg: int) -> Optional[int]:
        return self.regs.get(reg)

    def registers_at_slot(self, idx: int) -> Iterable[int]:
        return (reg for reg, slot in self.regs.items() if slot == idx)
