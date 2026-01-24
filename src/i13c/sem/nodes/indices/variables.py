from typing import Dict, Tuple

from i13c.core.mapping import OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.functions import Function, FunctionId
from i13c.sem.typing.entities.parameters import ParameterId
from i13c.sem.typing.indices.variables import Variable, VariableId


def configure_variables_by_parameters() -> Configuration:
    return Configuration(
        builder=build_variables_by_parameters,
        produces=(
            "entities/variables",
            "indices/variables-by-parameter",
        ),
        requires=frozenset({("functions", "entities/functions")}),
    )


def build_variables_by_parameters(
    functions: OneToOne[FunctionId, Function],
) -> Tuple[OneToOne[VariableId, Variable], OneToOne[ParameterId, VariableId]]:

    variables: Dict[VariableId, Variable] = {}
    parameters: Dict[ParameterId, VariableId] = {}

    for fid, function in functions.items():
        for pid in function.parameters:
            # for now we reuse parameter IDs
            vid = VariableId(value=pid.value)

            # add to the mapping
            parameters[pid] = vid

            # create the variable
            variables[vid] = Variable(
                kind="parameter",
                source=pid,
            )

    return (
        OneToOne[VariableId, Variable].instance(variables),
        OneToOne[ParameterId, VariableId].instance(parameters),
    )
