from collections.abc import Callable
from dataclasses import dataclass

from i13c.semantic.typing.analyses import llvm

ShuffleInstruction = llvm.MOV | llvm.XCHG


@dataclass(kw_only=True)
class ShuffleSegment:
    before: list[ShuffleInstruction]
    after: list[ShuffleInstruction]


@dataclass(kw_only=True)
class Shuffle:
    segments: list[ShuffleSegment | None]
    transfer: Transfer


@dataclass(kw_only=True)
class InRegister:
    name: bytes

    def __str__(self) -> str:
        return self.name.decode()


@dataclass(kw_only=True)
class InMemory:
    slot: int

    def __str__(self) -> str:
        return f"#{self.slot:04d}"


Location = InRegister | InMemory
Coloring = dict[bytes, Location]

# shuffle instruction transfer function type
Transfer = Callable[[InRegister, Coloring, Coloring], list[ShuffleInstruction]]
