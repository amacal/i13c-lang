from typing import Dict, Protocol

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Hex, Type
from i13c.semantic.typing.entities.callsites import Argument, CallSite, CallSiteId
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.literals import Literal, LiteralId
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.indices.controlflows import FlowNode
from i13c.semantic.typing.indices.environments import Environment
from i13c.semantic.typing.indices.variables import Variable, VariableId
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution


def configure_resolution_by_callsite() -> GraphNode:
    return GraphNode(
        builder=build_resolution_by_callsite,
        constraint=None,
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


def match_variable(variable: Variable, type: Type) -> bool:
    # width constraint
    if variable.type.width > type.width:
        return False

    # lower bound constraint
    if Hex.lesser(variable.type.range.lower.data, type.range.lower.data):
        return False

    # upper bound constraint
    if Hex.greater(variable.type.range.upper.data, type.range.upper.data):
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


    return OneToOne[CallSiteId, CallSiteResolution].instance(resolutions)
