from typing import Dict, List

from i13c.core.mapping import OneToOne
from i13c.sem.core import Identifier, Type, default_ranges, width_from_ranges
from i13c.sem.infra import Configuration
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.functions import (
    Function,
    FunctionId,
    Parameter,
    Statement,
)


def configure_functions() -> Configuration:
    return Configuration(
        builder=build_functions,
        produces=("entities/functions",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_functions(
    graph: SyntaxGraph,
) -> OneToOne[FunctionId, Function]:
    functions: Dict[FunctionId, Function] = {}

    for nid, function in graph.functions.items():
        parameters: List[Parameter] = []
        statements: List[Statement] = []

        for parameter in function.parameters:
            # default width and ranges for declared type
            ranges = default_ranges(parameter.type.name)

            # override ranges if specified
            if parameter.type.range is not None:
                ranges = (parameter.type.range.lower, parameter.type.range.upper)

            # derive width from ranges
            width = width_from_ranges(*ranges)

            # construct slot type with range or default width
            type = Type(
                name=parameter.type.name,
                width=width,
                lower=parameter.type.range.lower if parameter.type.range else ranges[0],
                upper=parameter.type.range.upper if parameter.type.range else ranges[1],
            )

            parameters.append(
                Parameter(
                    name=Identifier(name=parameter.name),
                    type=type,
                )
            )

        for statement in function.statements:
            sid = graph.statements.get_by_node(statement)
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

    return OneToOne[FunctionId, Function].instance(functions)
