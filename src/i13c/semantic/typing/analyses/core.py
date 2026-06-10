from dataclasses import dataclass
from typing import Optional

from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet, AsmletId
from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.analyses.cflows import ControlFlows
from i13c.semantic.typing.analyses.cgraphs import CallGraph
from i13c.semantic.typing.analyses.cpaths import ControlPaths
from i13c.semantic.typing.analyses.entrypoints import Entrypoint
from i13c.semantic.typing.analyses.noreturns import NoReturn
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId


@dataclass
class AnalysisNodes:
    asmlets: Optional[OneToOne[AsmletId, Asmlet]]
    callings: Optional[OneToOne[CallSiteId, Calling]]
    cflows: OneToOne[FunctionId, ControlFlows]
    cgraphs: Optional[OneToOne[SignatureId, CallGraph]]
    cpaths: Optional[OneToOne[FunctionId, ControlPaths]]
    entrypoints: Optional[OneToOne[SignatureId, Entrypoint]]
    noreturns: Optional[OneToOne[SignatureId, NoReturn]]
