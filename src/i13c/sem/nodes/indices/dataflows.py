from typing import Dict, List

from i13c.core.mapping import OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.functions import Function, FunctionId
from i13c.sem.typing.entities.parameters import ParameterId
from i13c.sem.typing.indices.controlflows import FlowEntry, FlowGraph, FlowNode
from i13c.sem.typing.indices.dataflows import DataFlow
from i13c.sem.typing.indices.variables import VariableId


def configure_dataflow_by_flownode() -> Configuration:
    return Configuration(
        builder=build_dataflows,
        produces=("indices/dataflow-by-flownode",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("controlflows", "indices/flowgraph-by-function"),
                ("variables", "indices/variables-by-parameter"),
            }
        ),
    )


def build_dataflows(
    functions: OneToOne[FunctionId, Function],
    controlflows: OneToOne[FunctionId, FlowGraph],
    variables: OneToOne[ParameterId, VariableId],
) -> OneToOne[FunctionId, FlowGraph]:

    # found dataflows for each entry
    dataflows: Dict[FlowNode, DataFlow] = {}

    for fid, function in functions.items():
        flowgraph = controlflows.get(fid)
        entry: FlowEntry = flowgraph.entry

        for node in flowgraph.nodes():
            dataflows[node] = DataFlow(
                declares=[],
                reads=[],
                writes=[],
            )

        for pid in function.parameters:
            vid = variables.get(pid)
            dataflows[entry].declares.append(vid)

    return OneToOne[FunctionId, FlowGraph].instance(dataflows)
