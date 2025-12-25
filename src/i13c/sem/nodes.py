from dataclasses import dataclass
from typing import List, Optional, Union

from i13c.sem import ids
from i13c.sem.types import Immediate, Literal, Register, Type


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
    value: Literal


@dataclass(kw_only=True)
class CallId:
    id: int


@dataclass(kw_only=True)
class Call:
    id: CallId
    name: bytes
    arguments: List[Argument]
    candidates: List[Function]


@dataclass(kw_only=True)
class InstructionId:
    id: int


@dataclass(kw_only=True)
class Instruction:
    id: InstructionId
    mnemonic: bytes
    operands: List[Union[Register, Immediate]]


@dataclass(kw_only=True)
class FunctionId:
    id: int


@dataclass(kw_only=True)
class Function:
    id: FunctionId
    name: bytes
    terminal: bool
    parameters: List[Parameter]
    clobbers: List[Register]
    body: List[Union[Instruction, Call]]
