from dataclasses import dataclass
from typing import Optional

from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet, AsmletId
from i13c.semantic.typing.analyses.cflows import ControlFlows
from i13c.semantic.typing.analyses.cgraphs import CallGraph
from i13c.semantic.typing.analyses.cpaths import ControlPaths
from i13c.semantic.typing.analyses.noreturns import NoReturn
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId


@dataclass
class AnalysisNodes:
    asmlets: Optional[OneToOne[AsmletId, Asmlet]]
    cflows: OneToOne[FunctionId, ControlFlows]
    cgraphs: Optional[OneToOne[SignatureId, CallGraph]]
    cpaths: Optional[OneToOne[FunctionId, ControlPaths]]
    noreturns: Optional[OneToOne[SignatureId, NoReturn]]
