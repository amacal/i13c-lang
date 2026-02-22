from typing import Set

from i13c.lowering.typing.registers import IR_REGISTER_FORWARD


def caller_saved() -> Set[int]:
    return set(range(0, 8)) - {IR_REGISTER_FORWARD[b"rsp"]}
