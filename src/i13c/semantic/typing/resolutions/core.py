from dataclasses import dataclass

from i13c.core.mapping import OneToOne
from i13c.semantic.typing.identifiers.addresses import AddressId
from i13c.semantic.typing.identifiers.assigns import AssignId
from i13c.semantic.typing.identifiers.binds import BindId
from i13c.semantic.typing.identifiers.calls import CallId
from i13c.semantic.typing.identifiers.callsites import CallSiteId
from i13c.semantic.typing.identifiers.displacements import DisplacementId
from i13c.semantic.typing.identifiers.environments import EnvironmentId
from i13c.semantic.typing.identifiers.expressions import ExpressionId
from i13c.semantic.typing.identifiers.flags import FlagsId
from i13c.semantic.typing.identifiers.functions import FunctionId
from i13c.semantic.typing.identifiers.immediates import ImmediateId
from i13c.semantic.typing.identifiers.indices import IndexId
from i13c.semantic.typing.identifiers.instructions import InstructionId
from i13c.semantic.typing.identifiers.labels import LabelId
from i13c.semantic.typing.identifiers.literals import LiteralId
from i13c.semantic.typing.identifiers.mnemonics import MnemonicId
from i13c.semantic.typing.identifiers.operands import OperandId
from i13c.semantic.typing.identifiers.parameters import ParameterId
from i13c.semantic.typing.identifiers.ranges import RangeId
from i13c.semantic.typing.identifiers.references import ReferenceId
from i13c.semantic.typing.identifiers.registers import RegisterId
from i13c.semantic.typing.identifiers.results import ResultId
from i13c.semantic.typing.identifiers.signatures import SignatureId
from i13c.semantic.typing.identifiers.snippets import SnippetId
from i13c.semantic.typing.identifiers.statements import StatementId
from i13c.semantic.typing.identifiers.types import TypeId
from i13c.semantic.typing.identifiers.usages import UsageId
from i13c.semantic.typing.identifiers.values import ValueId
from i13c.semantic.typing.resolutions.addresses import AddressResolution
from i13c.semantic.typing.resolutions.assigns import AssignResolution
from i13c.semantic.typing.resolutions.bindings import BindingResolution
from i13c.semantic.typing.resolutions.binds import BindResolution
from i13c.semantic.typing.resolutions.calls import CallResolution
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution
from i13c.semantic.typing.resolutions.cflows import ControlFlowResolution
from i13c.semantic.typing.resolutions.displacements import DisplacementResolution
from i13c.semantic.typing.resolutions.environments import EnvironmentResolution
from i13c.semantic.typing.resolutions.expressions import ExpressionResolution
from i13c.semantic.typing.resolutions.flags import FlagsResolution
from i13c.semantic.typing.resolutions.functions import FunctionResolution
from i13c.semantic.typing.resolutions.immediates import ImmediateResolution
from i13c.semantic.typing.resolutions.indices import IndexResolution
from i13c.semantic.typing.resolutions.instructions import InstructionResolution
from i13c.semantic.typing.resolutions.labels import LabelResolution
from i13c.semantic.typing.resolutions.literals import LiteralResolution
from i13c.semantic.typing.resolutions.mnemonics import MnemonicResolution
from i13c.semantic.typing.resolutions.operands import OperandResolution
from i13c.semantic.typing.resolutions.parameters import ParameterResolution
from i13c.semantic.typing.resolutions.ranges import RangeResolution
from i13c.semantic.typing.resolutions.references import ReferenceResolution
from i13c.semantic.typing.resolutions.registers import RegisterResolution
from i13c.semantic.typing.resolutions.results import ResultResolution
from i13c.semantic.typing.resolutions.signatures import SignatureResolution
from i13c.semantic.typing.resolutions.snippets import SnippetResolution
from i13c.semantic.typing.resolutions.statements import StatementResolution
from i13c.semantic.typing.resolutions.types import TypeResolution
from i13c.semantic.typing.resolutions.usages import UsageResolution
from i13c.semantic.typing.resolutions.values import ValueResolution


@dataclass(repr=False)
class ResolutionNodes:
    assigns: OneToOne[AssignId, AssignResolution] | None
    addresses: OneToOne[AddressId, AddressResolution] | None
    bindings: OneToOne[SignatureId, BindingResolution] | None
    binds: OneToOne[BindId, BindResolution] | None
    calls: OneToOne[CallId, CallResolution] | None
    callsites: OneToOne[CallSiteId, CallSiteResolution] | None
    cflows: OneToOne[FunctionId, ControlFlowResolution] | None
    displacements: OneToOne[DisplacementId, DisplacementResolution] | None
    environments: OneToOne[EnvironmentId, EnvironmentResolution] | None
    usages: OneToOne[UsageId, UsageResolution] | None
    flags: OneToOne[FlagsId, FlagsResolution] | None
    functions: OneToOne[FunctionId, FunctionResolution] | None
    immediates: OneToOne[ImmediateId, ImmediateResolution] | None
    indices: OneToOne[IndexId, IndexResolution] | None
    instructions: OneToOne[InstructionId, InstructionResolution] | None
    labels: OneToOne[LabelId, LabelResolution] | None
    literals: OneToOne[LiteralId, LiteralResolution] | None
    mnemonics: OneToOne[MnemonicId, MnemonicResolution] | None
    operands: OneToOne[OperandId, OperandResolution] | None
    ranges: OneToOne[RangeId, RangeResolution] | None
    references: OneToOne[ReferenceId, ReferenceResolution] | None
    registers: OneToOne[RegisterId, RegisterResolution] | None
    results: OneToOne[ResultId, ResultResolution] | None
    signatures: OneToOne[SignatureId, SignatureResolution] | None
    statements: OneToOne[StatementId, StatementResolution] | None
    expressions: OneToOne[ExpressionId, ExpressionResolution] | None
    parameters: OneToOne[ParameterId, ParameterResolution] | None
    snippets: OneToOne[SnippetId, SnippetResolution] | None
    types: OneToOne[TypeId, TypeResolution] | None
    values: OneToOne[ValueId, ValueResolution] | None
