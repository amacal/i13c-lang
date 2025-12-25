from dataclasses import dataclass

from i13c.sem.graph import ArgumentId, CallId, FunctionId, ParameterId


@dataclass(kw_only=True)
class Type:
    name: bytes


@dataclass(kw_only=True)
class Register:
    name: bytes


@dataclass(kw_only=True, frozen=True)
class CallSite:
    call: CallId
    function: FunctionId


@dataclass(kw_only=True, frozen=True)
class SlotBinding:
    argument: ArgumentId
    parameter: ParameterId
