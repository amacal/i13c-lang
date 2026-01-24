from typing import Dict

from i13c.core.mapping import OneToOne
from i13c.sem.core import Identifier, Range, Type, default_range, width_from_range
from i13c.sem.infra import Configuration
from i13c.sem.syntax import SyntaxGraph
from i13c.sem.typing.entities.variables import Variable, VariableId


def configure_variables() -> Configuration:
    return Configuration(
        builder=build_variables,
        produces=("entities/variables",),
        requires=frozenset({("graph", "syntax/graph")}),
    )


def build_variables(
    graph: SyntaxGraph,
) -> OneToOne[VariableId, Variable]:
    variables: Dict[VariableId, Variable] = {}

    for pid, parameter in graph.parameters.items():
        # derive parameter ID from globally unique node ID
        variable_id = VariableId(value=pid.value)

        # default width and ranges for declared type
        range: Range = default_range(parameter.type.name)

        # override ranges if specified
        if parameter.type.range is not None:
            range = Range(
                lower=parameter.type.range.lower,
                upper=parameter.type.range.upper,
            )

        # derive width from ranges
        width = width_from_range(range)

        # construct slot type with range or default width
        type = Type(
            name=parameter.type.name,
            width=width,
            range=range,
        )

        variables[variable_id] = Variable(
            ref=parameter.ref,
            type=type,
            owner=None,
            ident=Identifier(name=parameter.name),
        )

    return OneToOne[VariableId, Variable].instance(variables)
