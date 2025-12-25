from dataclasses import dataclass
from typing import List, Tuple, Type, Union

from i13c.sem.nodes import Immediate, Register

AllowedVariants = Union[Type[Register], Type[Immediate]]


@dataclass(kw_only=True)
class InstructionSignature:
    variants: List[Tuple[AllowedVariants, ...]]


INSTRUCTIONS_TABLE = {
    b"syscall": InstructionSignature(variants=[()]),
    b"mov": InstructionSignature(variants=[(Register, Immediate)]),
}
