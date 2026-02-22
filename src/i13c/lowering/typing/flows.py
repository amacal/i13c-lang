from dataclasses import dataclass
from typing import Tuple, Union

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


@dataclass(kw_only=True)
class BindingFlow:
    dst: int
    src: ExpressionId


@dataclass(kw_only=True)
class PrologueFlow:
    target: FunctionId

    def __str__(self) -> str:
        return f"PrologueFlow({self.target.identify(1)})"


@dataclass(kw_only=True)
class EpilogueFlow:
    target: FunctionId

    def __str__(self) -> str:
        return f"EpilogueFlow({self.target.identify(1)})"


@dataclass(kw_only=True)
class PreserveFlow:
    pass


@dataclass(kw_only=True)
class RestoreFlow:
    pass


Flow = Union[
    CallFlow, BindingFlow, PrologueFlow, EpilogueFlow, PreserveFlow, RestoreFlow
]


@dataclass(kw_only=True, frozen=True)
class FlowId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("flow", f"{self.value:<{length}}"))


FlowEntry = Tuple[FlowId, Flow]
