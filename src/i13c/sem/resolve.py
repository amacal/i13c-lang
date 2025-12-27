from dataclasses import dataclass
from typing import Dict, Iterable, List
from typing import Literal as Kind
from typing import Optional, Tuple

from i13c.sem.callable import Callable
from i13c.sem.callsite import Argument, CallSite, CallSiteId
from i13c.sem.core import Type
from i13c.sem.function import Function, FunctionId
from i13c.sem.literal import Hex, Literal, LiteralId
from i13c.sem.snippet import Snippet, SnippetId

RejectionReason = Kind[
    b"wrong-arity",
    b"type-mismatch",
]


@dataclass(kw_only=True)
class Rejection:
    callable: Callable
    reason: RejectionReason


@dataclass(kw_only=True)
class Acceptance:
    callable: Callable


@dataclass(kw_only=True)
class Resolution:
    accepted: List[Acceptance]
    rejected: List[Rejection]


def build_resolutions(
    functions: Dict[FunctionId, Function],
    snippets: Dict[SnippetId, Snippet],
    callsites: Dict[CallSiteId, CallSite],
    literals: Dict[LiteralId, Literal],
) -> Dict[CallSiteId, Resolution]:
    resolutions: Dict[CallSiteId, Resolution] = {}

    def match_literal(literal: Literal, type: Type) -> bool:
        match (type.name, literal.kind):
            case (b"u8", b"hex"):
                assert isinstance(literal.target, Hex)
                return literal.target.width is not None and literal.target.width <= 8

            case (b"u16", b"hex"):
                assert isinstance(literal.target, Hex)
                return literal.target.width is not None and literal.target.width <= 16

            case (b"u32", b"hex"):
                assert isinstance(literal.target, Hex)
                return literal.target.width is not None and literal.target.width <= 32

            case (b"u64", b"hex"):
                assert isinstance(literal.target, Hex)
                return literal.target.width is not None and literal.target.width <= 64

            case _:
                return False

    def match_bindings(
        bindings: Iterable[Tuple[Argument, Type]],
    ) -> Optional[RejectionReason]:
        for argument, parameter in bindings:
            match argument:
                case Argument(kind=b"literal", target=lit):
                    assert isinstance(lit, LiteralId)
                    if not match_literal(literals[lit], type=parameter):
                        return b"type-mismatch"
                case _:
                    return b"type-mismatch"

        return None

    def match_function(
        callsite: CallSite, function: Function
    ) -> Optional[RejectionReason]:
        if len(function.parameters) != len(callsite.arguments):
            return b"wrong-arity"

        return match_bindings(
            zip(
                callsite.arguments,
                [parameter.type for parameter in function.parameters],
            )
        )

    def match_snippet(
        callsite: CallSite, snippet: Snippet
    ) -> Optional[RejectionReason]:
        if len(snippet.slots) != len(callsite.arguments):
            return b"wrong-arity"

        return match_bindings(
            zip(callsite.arguments, [slot.type for slot in snippet.slots])
        )

    def match_callable(
        callsite: CallSite, callable: Callable
    ) -> Optional[RejectionReason]:
        match callable:
            case Callable(kind=b"function", target=target):
                assert isinstance(target, FunctionId)
                return match_function(callsite, functions[target])
            case Callable(kind=b"snippet", target=target):
                assert isinstance(target, SnippetId)
                return match_snippet(callsite, snippets[target])
            case _:
                return None

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

        reasoned: List[Tuple[Callable, Optional[RejectionReason]]] = [
            (candidate, match_callable(callsites[cid], candidate))
            for candidate in candidates
        ]

        resolutions[cid] = Resolution(
            accepted=[
                Acceptance(callable=candidate)
                for candidate, reason in reasoned
                if reason is None
            ],
            rejected=[
                Rejection(callable=candidate, reason=reason)
                for candidate, reason in reasoned
                if reason is not None
            ],
        )

    return resolutions
