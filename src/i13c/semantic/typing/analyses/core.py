from dataclasses import dataclass

from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.asmlets import Asmlet
from i13c.semantic.typing.analyses.assigns import AssignLlvm
from i13c.semantic.typing.analyses.callings import Calling
from i13c.semantic.typing.analyses.calls import CallLlvm
from i13c.semantic.typing.analyses.cflows import ControlFlows
from i13c.semantic.typing.analyses.cgraphs import CallGraph
from i13c.semantic.typing.analyses.cpaths import ControlPaths
from i13c.semantic.typing.analyses.dflows import DataFlows
from i13c.semantic.typing.analyses.entrypoints import Entrypoint
from i13c.semantic.typing.analyses.fnlets import Fnlet
from i13c.semantic.typing.analyses.noreturns import NoReturn
from i13c.semantic.typing.analyses.sections import Section
from i13c.semantic.typing.analyses.shuffles import Shuffle
from i13c.semantic.typing.analyses.statements import StatementLlvm
from i13c.semantic.typing.identifiers.asmlets import AsmletId
from i13c.semantic.typing.identifiers.assigns import AssignId
from i13c.semantic.typing.identifiers.calls import CallId
from i13c.semantic.typing.identifiers.callsites import CallSiteId
from i13c.semantic.typing.identifiers.functions import FunctionId
from i13c.semantic.typing.identifiers.sections import SectiontId
from i13c.semantic.typing.identifiers.signatures import SignatureId
from i13c.semantic.typing.identifiers.statements import StatementId


@dataclass(repr=False)
class AnalysisNodes:
    asmlets: OneToOne[AsmletId, Asmlet] | None
    assigns: OneToOne[AssignId, AssignLlvm] | None
    callings: OneToOne[CallSiteId, Calling] | None
    calls: OneToOne[CallId, CallLlvm] | None
    cflows: OneToOne[FunctionId, ControlFlows] | None
    cgraphs: OneToOne[SignatureId, CallGraph] | None
    cpaths: OneToOne[FunctionId, ControlPaths] | None
    dflows: OneToOne[FunctionId, DataFlows] | None
    entrypoints: OneToOne[SignatureId, Entrypoint] | None
    fnlets: OneToOne[FunctionId, Fnlet] | None
    noreturns: OneToOne[SignatureId, NoReturn] | None
    sections: OneToOne[SectiontId, Section] | None
    shuffles: OneToOne[FunctionId, Shuffle] | None
    statements: OneToOne[StatementId, StatementLlvm] | None
