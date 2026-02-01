from typing import Dict

from i13c.core.mapping import OneToOne
from i13c.sem.core import Identifier
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.functions import Function, FunctionId
from i13c.sem.typing.indices.controlflows import FlowEntry, FlowGraph, FlowNode
from i13c.sem.typing.indices.dataflows import DataFlow
from i13c.sem.typing.indices.environments import Environment
from i13c.sem.typing.indices.variables import Variable, VariableId


def configure_environment_by_flownode() -> Configuration:
    return Configuration(
        builder=build_environments,
        produces=("indices/environment-by-flownode",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("dataflows", "indices/dataflow-by-flownode"),
                ("controlflows", "indices/flowgraph-by-function"),
                ("variables", "entities/variables"),
            }
        ),
    )


def build_environments(
    functions: OneToOne[FunctionId, Function],
    dataflows: OneToOne[FlowNode, DataFlow],
    controlflows: OneToOne[FunctionId, FlowGraph],
    variables: OneToOne[VariableId, Variable],
) -> OneToOne[FlowNode, Environment]:

    # found environments for each flow node
    environments: Dict[FlowNode, Environment] = {}

    # process each function
    for fid in functions.keys():
        flowgraph = controlflows.get(fid)
        node: FlowNode = flowgraph.entry

        # collect intitial environment
        env = collect_entry(variables, dataflows, flowgraph.entry)
        environments[flowgraph.entry] = Environment(owner=fid, variables=env)

        while node != flowgraph.exit:
            for successor in flowgraph.forward.get(node, [flowgraph.exit]):
                node = successor

            # just clone current environment for now
            environments[node] = Environment(owner=fid, variables=dict(env))

    return OneToOne[FlowNode, Environment].instance(environments)


def collect_entry(
    variables: OneToOne[VariableId, Variable],
    dataflows: OneToOne[FlowNode, DataFlow],
    entry: FlowEntry,
) -> Dict[Identifier, VariableId]:
    # get the dataflow at the node
    dataflow = dataflows.get(entry)
    available: Dict[Identifier, VariableId] = {}

    # collect declared variables
    for vid in dataflow.declares:
        variable = variables.get(vid)
        available[variable.ident] = vid

    # return the available variables
    return available
