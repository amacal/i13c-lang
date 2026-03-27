from dataclasses import dataclass
from typing import Dict, Set

# fmt: off
IR_REGISTER_FORWARD: Dict[bytes, int] = {
    b"rax": 0, b"rcx": 1, b"rdx": 2, b"rbx": 3, b"rsp": 4, b"rbp": 5, b"rsi": 6, b"rdi": 7,
    b"r8": 8, b"r9": 9, b"r10": 10, b"r11": 11, b"r12": 12, b"r13": 13, b"r14": 14, b"r15": 15,
}
# fmt: on

# fmt: off
IR_REGISTER_BACKWARD: Dict[int, bytes] = {
    0: b"rax", 1: b"rcx", 2: b"rdx", 3: b"rbx", 4: b"rsp", 5: b"rbp", 6: b"rsi", 7: b"rdi",
    8: b"r8", 9: b"r9", 10: b"r10", 11: b"r11", 12: b"r12", 13: b"r13", 14: b"r14", 15: b"r15",
}
# fmt: on
def reg_to_name(reg: int) -> str:
    return IR_REGISTER_BACKWARD[reg].decode() if reg >= 0 else f"v{abs(reg)}"


def name_to_reg(name: str) -> int:
    return IR_REGISTER_FORWARD[name.encode()]


def caller_saved() -> Set[int]:
    return set(range(0, 8)) - {IR_REGISTER_FORWARD[b"rsp"]}


@dataclass(kw_only=True)
class VirtualRegister:
    id: int

    def ref(self) -> int:
        return -self.id

    def __str__(self) -> str:
        return f"v{self.id}"
