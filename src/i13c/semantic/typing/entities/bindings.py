from dataclasses import dataclass
from typing import List, Union

from i13c.semantic.typing.entities.callables import Callable
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.indices.variables import VariableId

CallSiteBindingTarget = Union[LiteralId, VariableId]


@dataclass(kw_only=True)
class CallSiteBindings:
    callable: Callable
    bindings: List[CallSiteBinding]


@dataclass(kw_only=True)
class CallSiteBinding:
    target: CallSiteBindingTarget
