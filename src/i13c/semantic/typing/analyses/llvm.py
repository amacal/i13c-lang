from dataclasses import dataclass

from i13c.semantic.core import Hex
from i13c.semantic.typing.analyses.asmlets import AsmletId
from i13c.semantic.typing.entities.functions import FunctionId


@dataclass(kw_only=True, repr=False)
class Immediate:
    value: Hex

    def __str__(self) -> str:
        return str(self.value)


@dataclass(kw_only=True, repr=False)
class Register:
    name: bytes

    def __str__(self) -> str:
        return self.name.decode("utf-8")


@dataclass(kw_only=True, repr=False)
class Slot:
    idx: int

    def __str__(self) -> str:
        return f"#{self.idx}"


@dataclass(kw_only=True, repr=False)
class Move:
    variant: tuple[Register, Register | Slot | Immediate] | tuple[Slot, Register]


@dataclass(kw_only=True, repr=False)
class Exchange:
    src: Register
    dst: Register


@dataclass(kw_only=True, repr=False)
class DecreaseStackPointer:
    slots: int


@dataclass(kw_only=True, repr=False)
class IncreaseStackPointer:
    slots: int


@dataclass(kw_only=True, repr=False)
class PushToStackPointer:
    src: Register


@dataclass(kw_only=True, repr=False)
class PopFromStackPointer:
    dst: Register


@dataclass(kw_only=True, repr=False)
class Call:
    target: AsmletId | FunctionId


@dataclass(kw_only=True, repr=False)
class Return:
    pass
