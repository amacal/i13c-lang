from typing import Dict, List

from i13c.core.mapping import OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.indices.controlflows import FlowGraph, FlowNode
from i13c.sem.typing.indices.dataflows import DataFlow


def configure_dataflow_by_flownode() -> Configuration:
    return Configuration(
        builder=build_dataflows,
        produces=("indices/dataflow-by-flownode",),
        requires=frozenset(
            {
                ("controlflows", "indices/flowgraph-by-function"),
            }
        ),
    )


def build_dataflows(
    controlflows: OneToOne[FunctionId, FlowGraph],
) -> OneToOne[FunctionId, FlowGraph]:

    dataflows: Dict[FlowNode, DataFlow] = {}

    for _, flows in controlflows.items():
        for node in flows.nodes():
            dataflows[node] = DataFlow(declares=[], reads=[], writes=[])

    return OneToOne[FunctionId, FlowGraph].instance(dataflows)
