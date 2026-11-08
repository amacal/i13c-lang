from dataclasses import dataclass

from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.addresses import Address
from i13c.semantic.typing.entities.assigns import Assign
from i13c.semantic.typing.entities.binds import Bind
from i13c.semantic.typing.entities.calls import Call
from i13c.semantic.typing.entities.callsites import CallSite
from i13c.semantic.typing.entities.displacements import Displacement
from i13c.semantic.typing.entities.environments import Environment
from i13c.semantic.typing.entities.expressions import Expression
from i13c.semantic.typing.entities.flags import Flags
from i13c.semantic.typing.entities.functions import Function
from i13c.semantic.typing.entities.immediates import Immediate
from i13c.semantic.typing.entities.indices import Index
from i13c.semantic.typing.entities.instructions import Instruction
from i13c.semantic.typing.entities.labels import Label
from i13c.semantic.typing.entities.literals import Literal
from i13c.semantic.typing.entities.mnemonics import Mnemonic
from i13c.semantic.typing.entities.operands import Operand
from i13c.semantic.typing.entities.parameters import Parameter
from i13c.semantic.typing.entities.ranges import Range
from i13c.semantic.typing.entities.references import Reference
from i13c.semantic.typing.entities.registers import Register
from i13c.semantic.typing.entities.results import Result
from i13c.semantic.typing.entities.signatures import Signature
from i13c.semantic.typing.entities.snippets import Snippet
from i13c.semantic.typing.entities.statements import Statement
from i13c.semantic.typing.entities.types import Type
from i13c.semantic.typing.entities.usages import Usage
from i13c.semantic.typing.entities.values import Value
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


@dataclass
class EntityNodes:
    addresses: OneToOne[AddressId, Address]
    assigns: OneToOne[AssignId, Assign]
    binds: OneToOne[BindId, Bind]
    calls: OneToOne[CallId, Call]
    callsites: OneToOne[CallSiteId, CallSite]
    displacements: OneToOne[DisplacementId, Displacement]
    environments: OneToOne[EnvironmentId, Environment]
    expressions: OneToOne[ExpressionId, Expression]
    usages: OneToOne[UsageId, Usage]
    flags: OneToOne[FlagsId, Flags]
    functions: OneToOne[FunctionId, Function]
    immediates: OneToOne[ImmediateId, Immediate]
    indices: OneToOne[IndexId, Index]
    instructions: OneToOne[InstructionId, Instruction]
    labels: OneToOne[LabelId, Label]
    literals: OneToOne[LiteralId, Literal]
    mnemonics: OneToOne[MnemonicId, Mnemonic]
    operands: OneToOne[OperandId, Operand]
    parameters: OneToOne[ParameterId, Parameter]
    ranges: OneToOne[RangeId, Range]
    references: OneToOne[ReferenceId, Reference]
    registers: OneToOne[RegisterId, Register]
    results: OneToOne[ResultId, Result]
    signatures: OneToOne[SignatureId, Signature]
    statements: OneToOne[StatementId, Statement]
    snippets: OneToOne[SnippetId, Snippet]
    types: OneToOne[TypeId, Type]
    values: OneToOne[ValueId, Value]
