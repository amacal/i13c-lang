from typing import Dict, List

from i13c import ast
from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Identifier
from i13c.semantic.syntax import SyntaxGraph
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import Function, FunctionId, Statement
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.values import ValueId


def configure_functions() -> GraphNode:
    return GraphNode(
        builder=build_functions,
        constraint=None,
        produces=("entities/functions",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_functions(
    graph: SyntaxGraph,
) -> OneToOne[FunctionId, Function]:
    functions: Dict[FunctionId, Function] = {}

    for nid, function in graph.functions.items():
        parameters: List[ParameterId] = []
        statements: List[Statement] = []

        for parameter in function.parameters:
            pid = graph.parameters.get_by_node(parameter)
            parameters.append(ParameterId(value=pid.value))

        for statement in function.statements:
            sid = graph.statements.get_by_node(statement)

            match statement:
                case ast.CallStatement():
                    statements.append(CallSiteId(value=sid.value))
                case ast.ValueStatement():
                    statements.append(ValueId(value=sid.value))

        # derive function ID from globally unique node ID
        function_id = FunctionId(value=nid.value)

        functions[function_id] = Function(
            ref=function.ref,
            identifier=Identifier(name=function.name),
            noreturn=function.noreturn,
            parameters=parameters,
            statements=statements,
        )

    return OneToOne[FunctionId, Function].instance(functions)
