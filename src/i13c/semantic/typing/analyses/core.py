from dataclasses import dataclass

from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.allocations import Allocation
from i13c.semantic.typing.analyses.asmlets import Asmlet, AsmletId
from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.analyses.cflows import ControlFlows
from i13c.semantic.typing.analyses.cgraphs import CallGraph
from i13c.semantic.typing.analyses.cpaths import ControlPaths
from i13c.semantic.typing.analyses.dflows import DataFlows
from i13c.semantic.typing.analyses.entrypoints import Entrypoint
from i13c.semantic.typing.analyses.frames import StackFrame
from i13c.semantic.typing.analyses.liveness import Liveness
from i13c.semantic.typing.analyses.noreturns import NoReturn
from i13c.semantic.typing.analyses.shuffles import Shuffle
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId


@dataclass
class AnalysisNodes:
    allocations: OneToOne[FunctionId, Allocation] | None
    asmlets: OneToOne[AsmletId, Asmlet] | None
    callings: OneToOne[CallSiteId, Calling] | None
    cflows: OneToOne[FunctionId, ControlFlows] | None
    cgraphs: OneToOne[SignatureId, CallGraph] | None
    cpaths: OneToOne[FunctionId, ControlPaths] | None
    dflows: OneToOne[FunctionId, DataFlows] | None
    entrypoints: OneToOne[SignatureId, Entrypoint] | None
    frames: OneToOne[FunctionId, StackFrame] | None
    liveness: OneToOne[FunctionId, Liveness] | None
    noreturns: OneToOne[SignatureId, NoReturn] | None
    shuffles: OneToOne[FunctionId, Shuffle] | None
