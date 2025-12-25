from dataclasses import dataclass

from i13c.sem import ids


@dataclass(kw_only=True)
class Type:
    name: bytes


@dataclass(kw_only=True)
class Register:
    name: bytes


@dataclass(kw_only=True, frozen=True)
class CallSite:
    call: ids.CallId
    function: ids.FunctionId


@dataclass(kw_only=True, frozen=True)
class SlotBinding:
    argument: ids.ArgumentId
    parameter: ids.ParameterId
