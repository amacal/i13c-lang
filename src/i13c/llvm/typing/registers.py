from dataclasses import dataclass
from typing import Dict, Set

# fmt: off
IR_REGISTER_FORWARD_8: Dict[bytes, int] = {
    b"al": 0, b"cl": 1, b"dl": 2, b"bl": 3, b"spl": 4, b"bpl": 5, b"sil": 6, b"dil": 7,
    b"r8b": 8, b"r9b": 9, b"r10b": 10, b"r11b": 11, b"r12b": 12, b"r13b": 13, b"r14b": 14, b"r15b": 15,
}

IR_REGISTER_FORWARD_16: Dict[bytes, int] = {
    b"ax": 0, b"cx": 1, b"dx": 2, b"bx": 3, b"sp": 4, b"bp": 5, b"si": 6, b"di": 7,
    b"r8w": 8, b"r9w": 9, b"r10w": 10, b"r11w": 11, b"r12w": 12, b"r13w": 13, b"r14w": 14, b"r15w": 15,
}

IR_REGISTER_FORWARD_32: Dict[bytes, int] = {
    b"eax": 0, b"ecx": 1, b"edx": 2, b"ebx": 3, b"esp": 4, b"ebp": 5, b"esi": 6, b"edi": 7,
    b"r8d": 8, b"r9d": 9, b"r10d": 10, b"r11d": 11, b"r12d": 12, b"r13d": 13, b"r14d": 14, b"r15d": 15,
}

IR_REGISTER_FORWARD_64: Dict[bytes, int] = {
    b"rax": 0, b"rcx": 1, b"rdx": 2, b"rbx": 3, b"rsp": 4, b"rbp": 5, b"rsi": 6, b"rdi": 7,
    b"r8": 8, b"r9": 9, b"r10": 10, b"r11": 11, b"r12": 12, b"r13": 13, b"r14": 14, b"r15": 15,
}

IR_REGISTER_BACKWARD_8: Dict[int, bytes] = {
    0: b"al", 1: b"cl", 2: b"dl", 3: b"bl", 4: b"spl", 5: b"bpl", 6: b"sil", 7: b"dil",
    8: b"r8b", 9: b"r9b", 10: b"r10b", 11: b"r11b", 12: b"r12b", 13: b"r13b", 14: b"r14b", 15: b"r15b",
}

IR_REGISTER_BACKWARD_16: Dict[int, bytes] = {
    0: b"ax", 1: b"cx", 2: b"dx", 3: b"bx", 4: b"sp", 5: b"bp", 6: b"si", 7: b"di",
    8: b"r8w", 9: b"r9w", 10: b"r10w", 11: b"r11w", 12: b"r12w", 13: b"r13w", 14: b"r14w", 15: b"r15w",
}

IR_REGISTER_BACKWARD_32: Dict[int, bytes] = {
    0: b"eax", 1: b"ecx", 2: b"edx", 3: b"ebx", 4: b"esp", 5: b"ebp", 6: b"esi", 7: b"edi",
    8: b"r8d", 9: b"r9d", 10: b"r10d", 11: b"r11d", 12: b"r12d", 13: b"r13d", 14: b"r14d", 15: b"r15d",
}

IR_REGISTER_BACKWARD_64: Dict[int, bytes] = {
    0: b"rax", 1: b"rcx", 2: b"rdx", 3: b"rbx", 4: b"rsp", 5: b"rbp", 6: b"rsi", 7: b"rdi",
    8: b"r8", 9: b"r9", 10: b"r10", 11: b"r11", 12: b"r12", 13: b"r13", 14: b"r14", 15: b"r15",
}
# fmt: on


def reg8_to_name(reg: int) -> str:
    return IR_REGISTER_BACKWARD_8[reg].decode() if reg >= 0 else f"v{abs(reg)}"


def reg16_to_name(reg: int) -> str:
    return IR_REGISTER_BACKWARD_16[reg].decode() if reg >= 0 else f"v{abs(reg)}"


def reg32_to_name(reg: int) -> str:
    return IR_REGISTER_BACKWARD_32[reg].decode() if reg >= 0 else f"v{abs(reg)}"


def reg64_to_name(reg: int) -> str:
    return IR_REGISTER_BACKWARD_64[reg].decode() if reg >= 0 else f"v{abs(reg)}"


def name_to_reg8(name: str) -> int:
    return IR_REGISTER_FORWARD_8[name.encode()]


def name_to_reg16(name: str) -> int:
    return IR_REGISTER_FORWARD_16[name.encode()]


def name_to_reg32(name: str) -> int:
    return IR_REGISTER_FORWARD_32[name.encode()]


def name_to_reg64(name: str) -> int:
    return IR_REGISTER_FORWARD_64[name.encode()]


def caller_saved() -> Set[int]:
    return set(range(0, 8)) - {IR_REGISTER_FORWARD_64[b"rsp"]}


@dataclass(kw_only=True)
class VirtualRegister:
    id: int

    def ref(self) -> int:
        return -self.id

    def __str__(self) -> str:
        return f"v{self.id}"
