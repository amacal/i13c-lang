from typing import Dict, Iterable, List, Protocol, Tuple

from i13c.core.mapping import OneToOne
from i13c.res import Err, Ok, Result
from i13c.sem.core import Type
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.callables import Callable
from i13c.sem.typing.entities.callsites import Argument, CallSite, CallSiteId
from i13c.sem.typing.entities.expressions import Expression, ExpressionId
from i13c.sem.typing.entities.functions import Function, FunctionId
from i13c.sem.typing.entities.literals import Hex, Literal, LiteralId
from i13c.sem.typing.entities.parameters import Parameter, ParameterId
from i13c.sem.typing.entities.snippets import Snippet, SnippetId
from i13c.sem.typing.indices.controlflows import FlowNode
from i13c.sem.typing.indices.environments import Environment
from i13c.sem.typing.indices.variables import Variable, VariableId
from i13c.sem.typing.resolutions.callsites import (
    CallSiteAcceptance,
    CallSiteBinding,
    CallSiteRejection,
    CallSiteRejectionReason,
    CallSiteResolution,
)


def configure_resolution_by_callsite() -> Configuration:
    return Configuration(
        builder=build_resolution_by_callsite,
        produces=("resolutions/callsites",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("snippets", "entities/snippets"),
                ("callsites", "entities/callsites"),
                ("literals", "entities/literals"),
                ("parameters", "entities/parameters"),
                ("variables", "entities/variables"),
                ("expressions", "entities/expressions"),
                ("environments", "indices/environment-by-flownode"),
            }
        ),
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
            if not (type.range.lower <= target.value <= type.range.upper):
                return False

            # success
            return True

        case _:
            return False


def match_variable(variable: Variable, type: Type) -> bool:
    # width constraint
    if variable.type.width > type.width:
        return False

    # range constraint
    if not (
        type.range.lower <= variable.type.range.lower
        and variable.type.range.upper <= type.range.upper
    ):
        return False

    # success
    return True


def build_resolution_by_callsite(
    functions: OneToOne[FunctionId, Function],
    snippets: OneToOne[SnippetId, Snippet],
    callsites: OneToOne[CallSiteId, CallSite],
    literals: OneToOne[LiteralId, Literal],
    parameters: OneToOne[ParameterId, Parameter],
    variables: OneToOne[VariableId, Variable],
    expressions: OneToOne[ExpressionId, Expression],
    environments: OneToOne[FlowNode, Environment],
) -> OneToOne[CallSiteId, CallSiteResolution]:
    resolutions: Dict[CallSiteId, CallSiteResolution] = {}

    def match_bindings(
        environment: Environment,
        bindings: Iterable[CallSiteBinding],
    ) -> Result[List[CallSiteBinding], CallSiteRejectionReason]:
        for binding in bindings:
            match binding.argument:
                case Argument(kind=b"literal", target=LiteralId() as lit):
                    if not match_literal(literals.get(lit), type=binding.type):
                        return Err(b"type-mismatch")

                case Argument(kind=b"expression", target=ExpressionId() as eid):
                    # first extract expression and variable from environment
                    expression = expressions.get(eid)
                    variable = environment.variables.get(expression.ident)

                    # check variable existence
                    if variable is None:
                        return Err(b"unknown-target")

                    # check type match
                    if not match_variable(variables.get(variable), type=binding.type):
                        return Err(b"type-mismatch")

                case _:
                    return Err(b"type-mismatch")

        return Ok(list(bindings))

    def match_function(
        callsite: CallSite,
        function: Function,
    ) -> Result[List[CallSiteBinding], CallSiteRejectionReason]:
        if len(function.parameters) != len(callsite.arguments):
            return Err(b"wrong-arity")

        # find actual parameter variables
        params = [parameters.get(pid) for pid in function.parameters]
        environment = environments.get(callsite.id)

        # combine as bindings
        bindings = [
            CallSiteBinding.parameter(parameter.type, argument, parameter)
            for argument, parameter in zip(callsite.arguments, params)
        ]

        return match_bindings(environment, bindings)

    def match_snippet(
        callsite: CallSite, snippet: Snippet
    ) -> Result[List[CallSiteBinding], CallSiteRejectionReason]:
        if len(snippet.slots) != len(callsite.arguments):
            return Err(b"wrong-arity")

        bindings = [
            CallSiteBinding.slot(slot.type, argument, slot)
            for argument, slot in zip(callsite.arguments, snippet.slots)
        ]

        return match_bindings(Environment.empty(), bindings)

    def match_callable(
        callsite: CallSite, callable: Callable
    ) -> Result[List[CallSiteBinding], CallSiteRejectionReason]:
        match callable:
            case Callable(kind=b"function", target=FunctionId() as target):
                return match_function(callsite, functions.get(target))
            case Callable(kind=b"snippet", target=SnippetId() as target):
                return match_snippet(callsite, snippets.get(target))
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

        reasoned: List[
            Tuple[Callable, Result[List[CallSiteBinding], CallSiteRejectionReason]]
        ] = [
            (candidate, match_callable(callsites.get(cid), candidate))
            for candidate in candidates
        ]

        resolutions[cid] = CallSiteResolution(
            accepted=[
                CallSiteAcceptance(callable=candidate, bindings=result.value)
                for candidate, result in reasoned
                if isinstance(result, Ok)
            ],
            rejected=[
                CallSiteRejection(callable=candidate, reason=result.error)
                for candidate, result in reasoned
                if isinstance(result, Err)
            ],
        )

    return OneToOne[CallSiteId, CallSiteResolution].instance(resolutions)
