from dataclasses import dataclass
from typing import List
from typing import Literal as Symbol
from typing import Optional, Union

from i13c.sem.types import Immediate, Literal, Register, Type
from i13c.src import Span


@dataclass(kw_only=True)
class ParameterId:
    id: int


@dataclass(kw_only=True)
class Parameter:
    id: ParameterId
    name: bytes
    type: Type
    bind: Optional[Register]


@dataclass(kw_only=True)
class ArgumentId:
    id: int


@dataclass(kw_only=True)
class Argument:
    id: ArgumentId
    ref: Span
    value: Literal


@dataclass(kw_only=True)
class ExitPoint:
    ref: Span
    statement: Optional[Union[Call, Instruction]]


@dataclass(kw_only=True)
class CallId:
    id: int


@dataclass(kw_only=True)
class Call:
    id: CallId
    ref: Span
    name: bytes
    arguments: List[Argument]
    candidates: List[Function]


@dataclass(kw_only=True)
class InstructionId:
    id: int


@dataclass(kw_only=True)
class Instruction:
    id: InstructionId
    ref: Span
    mnemonic: bytes
    operands: List[Union[Register, Immediate]]


@dataclass(kw_only=True)
class FunctionId:
    id: int


@dataclass(kw_only=True)
class Function:
    id: FunctionId
    kind: Symbol["function", "snippet"]
    ref: Span
    name: bytes
    noreturn: bool
    parameters: List[Parameter]
    clobbers: List[Register]
    body: List[Union[Instruction, Call]]
    exit_points: List[ExitPoint]
