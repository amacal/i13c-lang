from dataclasses import dataclass
from typing import List, Union

from i13c.semantic.typing.entities.callables import Callable
from i13c.semantic.typing.entities.literals import LiteralId
from i13c.semantic.typing.entities.parameters import Parameter
from i13c.semantic.typing.entities.snippets import Slot
from i13c.semantic.typing.indices.variables import VariableId

CallSiteBindingSurce = Union[LiteralId, VariableId]
CallSiteBindingDestination = Union[Parameter, Slot]


@dataclass(kw_only=True)
class CallSiteBindings:
    callable: Callable
    entries: List[CallSiteBinding]


@dataclass(kw_only=True)
class CallSiteBinding:
    src: CallSiteBindingSurce
    dst: CallSiteBindingDestination
