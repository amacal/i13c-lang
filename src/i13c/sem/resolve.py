from dataclasses import dataclass
from typing import Dict, Iterable, List
from typing import Literal as Kind
from typing import Protocol, Tuple, Union

from i13c.res import Err, Ok, Result
from i13c.sem.callable import Callable
from i13c.sem.callsite import Argument, CallSite, CallSiteId
from i13c.sem.core import Type
from i13c.sem.function import Function, FunctionId, Parameter
from i13c.sem.literal import Hex, Literal, LiteralId
from i13c.sem.snippet import Slot, Snippet, SnippetId

RejectionReason = Kind[
    b"wrong-arity",
    b"type-mismatch",
    b"unknown-target",
]

BindingKind = Kind[
    b"argument",
    b"slot",
]


@dataclass(kw_only=True)
class Binding:
    kind: BindingKind
    type: Type
    argument: Argument
    target: Union[Parameter, Slot]

    @staticmethod
    def slot(type: Type, argument: Argument, target: Slot) -> "Binding":
        return Binding(kind=b"slot", type=type, argument=argument, target=target)

    @staticmethod
    def parameter(type: Type, argument: Argument, target: Parameter) -> "Binding":
        return Binding(kind=b"argument", type=type, argument=argument, target=target)


@dataclass(kw_only=True)
class Rejection:
    callable: Callable
    reason: RejectionReason


@dataclass(kw_only=True)
class Acceptance:
    callable: Callable
    bindings: List[Binding]

    def describe(self) -> str:
        return self.callable.describe()


@dataclass(kw_only=True)
class Resolution:
    accepted: List[Acceptance]
    rejected: List[Rejection]

    def describe(self) -> str:
        candidate = ""

        if len(self.accepted) > 0:
            candidate = self.accepted[0].describe()

        return (
            f"accepted={len(self.accepted)} rejected={len(self.rejected)} {candidate}"
        )


class BindingLike(Protocol):
    type: Type
    argument: Argument


def match_literal(literal: Literal, type: Type) -> bool:
    match literal:
        case Literal(kind=b"hex", target=Hex() as target):
            # width constraint
            if target.width > type.width:
                return False

            # range constraint
            if not (type.lower <= target.value <= type.upper):
                return False

            # success
            return True

        case _:
            return False


def build_resolutions(
    functions: Dict[FunctionId, Function],
    snippets: Dict[SnippetId, Snippet],
    callsites: Dict[CallSiteId, CallSite],
    literals: Dict[LiteralId, Literal],
) -> Dict[CallSiteId, Resolution]:
    resolutions: Dict[CallSiteId, Resolution] = {}

    def match_bindings(
        bindings: Iterable[Binding],
    ) -> Result[List[Binding], RejectionReason]:
        for binding in bindings:
            match binding.argument:
                case Argument(kind=b"literal", target=LiteralId() as lit):
                    if not match_literal(literals[lit], type=binding.type):
                        return Err(b"type-mismatch")
                case _:
                    return Err(b"type-mismatch")

        return Ok(list(bindings))

    def match_function(
        callsite: CallSite, function: Function
    ) -> Result[List[Binding], RejectionReason]:
        if len(function.parameters) != len(callsite.arguments):
            return Err(b"wrong-arity")

        bindings = [
            Binding.parameter(parameter.type, argument, parameter)
            for argument, parameter in zip(callsite.arguments, function.parameters)
        ]

        return match_bindings(bindings)

    def match_snippet(
        callsite: CallSite, snippet: Snippet
    ) -> Result[List[Binding], RejectionReason]:
        if len(snippet.slots) != len(callsite.arguments):
            return Err(b"wrong-arity")

        bindings = [
            Binding.slot(slot.type, argument, slot)
            for argument, slot in zip(callsite.arguments, snippet.slots)
        ]

        return match_bindings(bindings)

    def match_callable(
        callsite: CallSite, callable: Callable
    ) -> Result[List[Binding], RejectionReason]:
        match callable:
            case Callable(kind=b"function", target=FunctionId() as target):
                return match_function(callsite, functions[target])
            case Callable(kind=b"snippet", target=SnippetId() as target):
                return match_snippet(callsite, snippets[target])
            case _:
                return Err(b"unknown-target")

    for cid, callsite in callsites.items():
        candidates: List[Callable] = []

        for fid, function in functions.items():
            if function.identifier == callsite.callee:
                candidates.append(
                    Callable(
                        kind=b"function",
                        target=fid,
                    )
                )

        for snid, snippet in snippets.items():
            if snippet.identifier == callsite.callee:
                candidates.append(
                    Callable(
                        kind=b"snippet",
                        target=snid,
                    )
                )

        reasoned: List[Tuple[Callable, Result[List[Binding], RejectionReason]]] = [
            (candidate, match_callable(callsites[cid], candidate))
            for candidate in candidates
        ]

        resolutions[cid] = Resolution(
            accepted=[
                Acceptance(callable=candidate, bindings=result.value)
                for candidate, result in reasoned
                if isinstance(result, Ok)
            ],
            rejected=[
                Rejection(callable=candidate, reason=result.error)
                for candidate, result in reasoned
                if isinstance(result, Err)
            ],
        )

    return resolutions
