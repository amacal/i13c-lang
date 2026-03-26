from dataclasses import dataclass
from typing import List, Tuple, Union

from i13c.lowering.typing.registers import reg_to_name
from i13c.semantic.typing.entities.functions import FunctionId


@dataclass(kw_only=True, frozen=True)
class BlockId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("block", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class SnapshotFlow:
    src: int
    dst: int

    def native(self) -> str:
        return f"snapshot {reg_to_name(self.dst)}, {reg_to_name(self.src)}"


@dataclass(kw_only=True)
class CallFlow:
    target: FunctionId

    def native(self) -> str:
        return f"call {self.target.identify(1)}"


@dataclass(kw_only=True)
class ClobbersFlow:
    clobbers: List[int]

    def native(self) -> str:
        return f"clobbers {', '.join(map(reg_to_name, sorted(self.clobbers)))}"


@dataclass(kw_only=True)
class BindingFlow:
    dst: int
    src: int

    def native(self) -> str:
        return f"bind {reg_to_name(self.dst)}, {reg_to_name(self.src)}"


@dataclass(kw_only=True)
class PrologueFlow:
    target: FunctionId

    def native(self) -> str:
        return f"prologue {self.target.identify(1)}"


@dataclass(kw_only=True)
class EpilogueFlow:
    target: FunctionId

    def native(self) -> str:
        return f"epilogue {self.target.identify(1)}"


@dataclass(kw_only=True)
class ImmediateFlow:
    imm: int
    dst: int

    def native(self) -> str:
        return f"immediate {reg_to_name(self.dst)}, {self.imm:#010x}"


@dataclass(kw_only=True)
class MoveFlow:
    src: int
    dst: int

    def native(self) -> str:
        return f"move {reg_to_name(self.dst)}, {reg_to_name(self.src)}"


Flow = Union[
    CallFlow,
    ClobbersFlow,
    BindingFlow,
    PrologueFlow,
    EpilogueFlow,
    SnapshotFlow,
    ImmediateFlow,
    MoveFlow,
]


@dataclass(kw_only=True, frozen=True)
class FlowId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("flow", f"{self.value:<{length}}"))


FlowEntry = Tuple[FlowId, Flow]
