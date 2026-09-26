from dataclasses import dataclass

from i13c.core.mapping import OneToOne
from i13c.llvm.typing.allocations import Allocation
from i13c.llvm.typing.cflows import ControlFlow
from i13c.llvm.typing.dflows import DataFlow
from i13c.llvm.typing.liveness import Liveness
from i13c.llvm.typing.shuffles import Shuffle
from i13c.semantic.typing.entities.functions import FunctionId


@dataclass(repr=False)
class LlvmNodes:
    allocations: OneToOne[FunctionId, Allocation] | None
    cflows: OneToOne[FunctionId, ControlFlow] | None
    dflows: OneToOne[FunctionId, DataFlow] | None
    liveness: OneToOne[FunctionId, Liveness] | None
    shuffles: OneToOne[FunctionId, Shuffle] | None
