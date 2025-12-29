from dataclasses import dataclass
from typing import Dict, List, Union

from i13c.sem.callsite import CallSiteId
from i13c.sem.core import Identifier, Type
from i13c.sem.syntax import SyntaxGraph
from i13c.src import Span

Statement = Union[CallSiteId]


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int


@dataclass(kw_only=True)
class Parameter:
    name: Identifier
    type: Type


@dataclass(kw_only=True)
class Function:
    ref: Span
    identifier: Identifier
    noreturn: bool
    parameters: List[Parameter]
    statements: List[Statement]


def build_functions(
    graph: SyntaxGraph,
) -> Dict[FunctionId, Function]:
    functions: Dict[FunctionId, Function] = {}

    for nid, function in graph.nodes.functions.items():
        parameters: List[Parameter] = []
        statements: List[Statement] = []

        for parameter in function.parameters:
            parameters.append(
                Parameter(
                    name=Identifier(name=parameter.name),
                    type=Type(name=parameter.type.name),
                )
            )

        for statement in function.statements:
            sid = graph.nodes.statements.get_by_node(statement)
            statements.append(CallSiteId(value=sid.value))

        # derive function ID from globally unique node ID
        function_id = FunctionId(value=nid.value)

        functions[function_id] = Function(
            ref=function.ref,
            identifier=Identifier(name=function.name),
            noreturn=function.noreturn,
            parameters=parameters,
            statements=statements,
        )

    return functions
