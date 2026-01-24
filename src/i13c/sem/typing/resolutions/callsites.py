from dataclasses import dataclass
from typing import List
from typing import Literal as Kind
from typing import Union

from i13c.sem.core import Type
from i13c.sem.typing.entities.callables import Callable
from i13c.sem.typing.entities.callsites import Argument
from i13c.sem.typing.entities.parameters import Parameter
from i13c.sem.typing.entities.snippets import Slot

CallSiteRejectionReason = Kind[
    b"wrong-arity",
    b"type-mismatch",
    b"unknown-target",
]

CallSiteBindingKind = Kind[
    b"argument",
    b"slot",
]


@dataclass(kw_only=True)
class CallSiteBinding:
    kind: CallSiteBindingKind
    type: Type
    argument: Argument
    target: Union[Parameter, Slot]

    @staticmethod
    def slot(type: Type, argument: Argument, target: Slot) -> CallSiteBinding:
        return CallSiteBinding(
            kind=b"slot", type=type, argument=argument, target=target
        )

    @staticmethod
    def parameter(type: Type, argument: Argument, target: Parameter) -> CallSiteBinding:
        return CallSiteBinding(
            kind=b"argument", type=type, argument=argument, target=target
        )


@dataclass(kw_only=True)
class CallSiteRejection:
    callable: Callable
    reason: CallSiteRejectionReason


@dataclass(kw_only=True)
class CallSiteAcceptance:
    callable: Callable
    bindings: List[CallSiteBinding]

    def describe(self) -> str:
        return self.callable.describe()


@dataclass(kw_only=True)
class CallSiteResolution:
    accepted: List[CallSiteAcceptance]
    rejected: List[CallSiteRejection]

    def describe(self) -> str:
        candidate = ""

        if len(self.accepted) > 0:
            candidate = self.accepted[0].describe()

        return (
            f"accepted={len(self.accepted)} rejected={len(self.rejected)} {candidate}"
        )
