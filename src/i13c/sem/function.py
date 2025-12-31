from dataclasses import dataclass
from typing import Dict, List, Union

from i13c.sem.callsite import CallSiteId
from i13c.sem.core import Identifier, Type, default_ranges, default_width
from i13c.sem.syntax import SyntaxGraph
from i13c.src import Span

Statement = Union[CallSiteId]


@dataclass(kw_only=True, frozen=True)
class FunctionId:
    value: int

    def identify(self, length: int) -> str:
        return "#".join(("function", f"{self.value:<{length}}"))


@dataclass(kw_only=True)
class Parameter:
    name: Identifier
    type: Type

    def signature(self) -> str:
        return f"{self.name}:{self.type}"


@dataclass(kw_only=True)
class Function:
    ref: Span
    identifier: Identifier
    noreturn: bool
    parameters: List[Parameter]
    statements: List[Statement]

    def signature(self) -> str:
        parameters = ", ".join([parameter.signature() for parameter in self.parameters])
        return f"{self.identifier.name.decode()}/{len(self.parameters)} ({parameters})"

    def describe(self) -> str:
        return f"name={self.identifier.name.decode()}/{len(self.parameters)}"


def build_functions(
    graph: SyntaxGraph,
) -> Dict[FunctionId, Function]:
    functions: Dict[FunctionId, Function] = {}

    for nid, function in graph.functions.items():
        parameters: List[Parameter] = []
        statements: List[Statement] = []

        for parameter in function.parameters:
            # default width for declared type
            width = default_width(parameter.type.name)
            ranges = default_ranges(parameter.type.name)

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

    return functions
