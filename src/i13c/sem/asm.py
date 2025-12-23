from dataclasses import dataclass
from typing import List, Tuple, Type, Union

from i13c import ast

AllowedVariants = Union[Type[ast.Register], Type[ast.Immediate]]


@dataclass(kw_only=True)
class InstructionSignature:
    variants: List[Tuple[AllowedVariants, ...]]


INSTRUCTIONS_TABLE = {
    b"syscall": InstructionSignature(variants=[()]),
    b"mov": InstructionSignature(variants=[(ast.Register, ast.Immediate)]),
}
