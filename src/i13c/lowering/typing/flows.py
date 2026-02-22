from dataclasses import dataclass
from typing import Tuple, Union

from i13c.lowering.typing.registers import IR_REGISTER_BACKWARD
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.functions import FunctionId


@dataclass(kw_only=True, frozen=True)
class BlockId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("block", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class CallFlow:
    target: FunctionId

    def native(self) -> str:
        return f"call {self.target.identify(1)}"


@dataclass(kw_only=True)
class BindingFlow:
    dst: int
    src: ExpressionId

    def native(self) -> str:
        dst = IR_REGISTER_BACKWARD[self.dst].decode()
        return f"bind {dst}, {self.src.identify(1)}"


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
class PreserveFlow:
    def native(self) -> str:
        return "preserve"


@dataclass(kw_only=True)
class RestoreFlow:
    def native(self) -> str:
        return "restore"


Flow = Union[
    CallFlow, BindingFlow, PrologueFlow, EpilogueFlow, PreserveFlow, RestoreFlow
]


@dataclass(kw_only=True, frozen=True)
class FlowId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("flow", f"{self.value:<{length}}"))


FlowEntry = Tuple[FlowId, Flow]
