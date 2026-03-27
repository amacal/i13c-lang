from typing import Dict, Tuple

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.parameters import Parameter, ParameterId
from i13c.semantic.typing.entities.values import Value, ValueId
from i13c.semantic.typing.indices.variables import Variable, VariableId, VariableSource

# builds a collection of variables for each parameter;
# also provides index to retrieve variable by parameter-id;


def configure_variables_by_parameters() -> GraphNode:
    return GraphNode(
        builder=build_variables_by_parameters,
        constraint=None,
        produces=(
            "entities/variables",
            "indices/variables-by-source",
        ),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("parameters", "entities/parameters"),
                ("values", "entities/values"),
            }
        ),
    )


def build_variables_by_parameters(
    functions: OneToOne[FunctionId, Function],
    parameters: OneToOne[ParameterId, Parameter],
    values: OneToOne[ValueId, Value],
) -> Tuple[OneToOne[VariableId, Variable], OneToOne[VariableSource, VariableId]]:

    variables: Dict[VariableId, Variable] = {}
    by_parameter: Dict[VariableSource, VariableId] = {}

    for _, function in functions.items():
        for pid in function.parameters:
            # for now we reuse parameter IDs
            vid = VariableId(value=pid.value)
            parameter = parameters.get(pid)

            # add to the source-to-variable mapping
            by_parameter[pid] = vid

            # create the variable
            variables[vid] = Variable(
                ref=parameter.ref,
                source=pid,
                type=parameter.type,
                kind=b"parameter",
                ident=parameter.ident,
            )

    for _, value in values.items():
        # for now we reuse value IDs
        vid = VariableId(value=value.id.value)

        # add to the source-to-variable mapping
        by_parameter[value.id] = vid

        # add to the mapping
        variables[vid] = Variable(
            ref=value.ref,
            source=value.id,
            type=value.type,
            kind=b"value",
            ident=value.ident,
        )

    return (
        OneToOne[VariableId, Variable].instance(variables),
        OneToOne[VariableSource, VariableId].instance(by_parameter),
    )
