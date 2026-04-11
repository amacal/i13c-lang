from dataclasses import dataclass

from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.bindings import CallSiteBindings
from i13c.semantic.typing.entities.binds import Bind, BindId
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.immediates import Immediate, ImmediateId
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.entities.literals import Literal, LiteralId
from i13c.semantic.typing.entities.operands import Operand, OperandId
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.ranges import Range, RangeId
from i13c.semantic.typing.entities.registers import Register, RegisterId
from i13c.semantic.typing.entities.signatures import Signature, SignatureId
from i13c.semantic.typing.entities.slots import Slot, SlotId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.entities.types import Type, TypeId
from i13c.semantic.typing.entities.values import Value, ValueId
from i13c.semantic.typing.indices.usages import Usage, UsageId
from i13c.semantic.typing.indices.variables import Variable, VariableId


@dataclass
class EntityNodes:
    bindings: OneToOne[CallSiteId, CallSiteBindings]
    binds: OneToOne[BindId, Bind]
    callsites: OneToOne[CallSiteId, CallSite]
    expressions: OneToOne[ExpressionId, Expression]
    functions: OneToOne[FunctionId, Function]
    immediates: OneToOne[ImmediateId, Immediate]
    instructions: OneToOne[InstructionId, Instruction]
    literals: OneToOne[LiteralId, Literal]
    operands: OneToOne[OperandId, Operand]
    parameters: OneToOne[ParameterId, Parameter]
    ranges: OneToOne[RangeId, Range]
    registers: OneToOne[RegisterId, Register]
    signatures: OneToOne[SignatureId, Signature]
    slots: OneToOne[SlotId, Slot]
    snippets: OneToOne[SnippetId, Snippet]
    types: OneToOne[TypeId, Type]
    usages: OneToOne[UsageId, Usage]
    values: OneToOne[ValueId, Value]
    variables: OneToOne[VariableId, Variable]
