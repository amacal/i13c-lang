from dataclasses import dataclass
from typing import Optional

from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.addresses import AddressId
from i13c.semantic.typing.entities.assigns import AssignId
from i13c.semantic.typing.entities.binds import BindId
from i13c.semantic.typing.entities.calls import CallId
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.environments import EnvironmentId
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.flags import FlagsId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.immediates import ImmediateId
from i13c.semantic.typing.entities.instructions import InstructionId
from i13c.semantic.typing.entities.labels import LabelId
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.mnemonics import MnemonicId
from i13c.semantic.typing.entities.operands import OperandId
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.ranges import RangeId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.entities.values import ValueId
from i13c.semantic.typing.resolutions.addresses import AddressResolution
from i13c.semantic.typing.resolutions.assigns import AssignResolution
from i13c.semantic.typing.resolutions.bindings import BindingResolution
from i13c.semantic.typing.resolutions.binds import BindResolution
from i13c.semantic.typing.resolutions.calls import CallResolution
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution
from i13c.semantic.typing.resolutions.cflows import ControlFlowResolution
from i13c.semantic.typing.resolutions.environments import EnvironmentResolution
from i13c.semantic.typing.resolutions.expressions import ExpressionResolution
from i13c.semantic.typing.resolutions.flags import FlagsResolution
from i13c.semantic.typing.resolutions.immediates import ImmediateResolution
from i13c.semantic.typing.resolutions.instructions import InstructionResolution
from i13c.semantic.typing.resolutions.labels import LabelResolution
from i13c.semantic.typing.resolutions.literals import LiteralResolution
from i13c.semantic.typing.resolutions.mnemonics import MnemonicResolution
from i13c.semantic.typing.resolutions.operands import OperandResolution
from i13c.semantic.typing.resolutions.parameters import ParameterResolution
from i13c.semantic.typing.resolutions.ranges import RangeResolution
from i13c.semantic.typing.resolutions.references import ReferenceResolution
from i13c.semantic.typing.resolutions.registers import RegisterResolution
from i13c.semantic.typing.resolutions.signatures import SignatureResolution
from i13c.semantic.typing.resolutions.snippets import SnippetResolution
from i13c.semantic.typing.resolutions.types import TypeResolution
from i13c.semantic.typing.resolutions.values import ValueResolution


@dataclass
class ResolutionNodes:
    assigns: Optional[OneToOne[AssignId, AssignResolution]]
    addresses: Optional[OneToOne[AddressId, AddressResolution]]
    bindings: Optional[OneToOne[SignatureId, BindingResolution]]
    binds: Optional[OneToOne[BindId, BindResolution]]
    calls: Optional[OneToOne[CallId, CallResolution]]
    callsites: Optional[OneToOne[CallSiteId, CallSiteResolution]]
    cflows: Optional[OneToOne[FunctionId, ControlFlowResolution]]
    environments: Optional[OneToOne[EnvironmentId, EnvironmentResolution]]
    expressions: Optional[OneToOne[ExpressionId, ExpressionResolution]]
    flags: Optional[OneToOne[FlagsId, FlagsResolution]]
    immediates: Optional[OneToOne[ImmediateId, ImmediateResolution]]
    instructions: Optional[OneToOne[InstructionId, InstructionResolution]]
    labels: Optional[OneToOne[LabelId, LabelResolution]]
    literals: Optional[OneToOne[LiteralId, LiteralResolution]]
    mnemonics: Optional[OneToOne[MnemonicId, MnemonicResolution]]
    operands: Optional[OneToOne[OperandId, OperandResolution]]
    ranges: Optional[OneToOne[RangeId, RangeResolution]]
    references: Optional[OneToOne[ReferenceId, ReferenceResolution]]
    registers: Optional[OneToOne[RegisterId, RegisterResolution]]
    signatures: Optional[OneToOne[SignatureId, SignatureResolution]]
    parameters: Optional[OneToOne[ParameterId, ParameterResolution]]
    snippets: Optional[OneToOne[SnippetId, SnippetResolution]]
    types: Optional[OneToOne[TypeId, TypeResolution]]
    values: Optional[OneToOne[ValueId, ValueResolution]]
