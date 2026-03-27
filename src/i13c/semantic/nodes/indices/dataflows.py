from typing import Dict

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.callsites import CallSite, CallSiteId
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.values import Value, ValueId
from i13c.semantic.typing.indices.controlflows import FlowGraph, FlowNode
from i13c.semantic.typing.indices.dataflows import DataFlow
from i13c.semantic.typing.indices.usages import UsageId
from i13c.semantic.typing.indices.variables import VariableId, VariableSource


def configure_dataflow_by_flownode() -> GraphNode:
    return GraphNode(
        builder=build_dataflows,
        constraint=None,
        produces=("indices/dataflow-by-flownode",),
        requires=frozenset(
            {
                ("functions", "entities/functions"),
                ("callsites", "entities/callsites"),
                ("controlflows", "indices/flowgraph-by-function"),
                ("variables", "indices/variables-by-source"),
                ("usages", "indices/usages-by-expression"),
                ("values", "entities/values"),
            }
        ),
    )


def build_dataflows(
    functions: OneToOne[FunctionId, Function],
    callsites: OneToOne[CallSiteId, CallSite],
    controlflows: OneToOne[FunctionId, FlowGraph],
    variables: OneToOne[VariableSource, VariableId],
    usages: OneToMany[ExpressionId, UsageId],
    values: OneToOne[ValueId, Value],
) -> OneToOne[FlowNode, DataFlow]:

    # found dataflows for each flow node
    dataflows: Dict[FlowNode, DataFlow] = {}

    # process each function
    for fid, function in functions.items():
        flowgraph = controlflows.get(fid)

        # each node produces a dataflow
        for node in flowgraph.nodes():
            dataflows[node] = DataFlow(
                declares=[],
                uses=[],
                drops=[],
            )

        # each parameter declares/drops a variable
        for pid in function.parameters:
            vid = variables.get(pid)
            dataflows[flowgraph.entry].declares.append(vid)
            dataflows[flowgraph.exit].drops.append(vid)

        # each callsite may read a variable
        for node in flowgraph.nodes():

            # handle callsites by looking up their arguments
            if isinstance(node, CallSiteId):
                callsite = callsites.get(node)

                for argument in callsite.arguments:
                    if argument.kind == b"expression":
                        assert isinstance(argument.target, ExpressionId)

                        # find usages of this expression
                        usage_ids = usages.get(argument.target)
                        dataflows[node].uses.extend(usage_ids)

            # handle values by looking up their expressions
            if isinstance(node, ValueId):
                value = values.get(node)

                if value.expr.kind == b"expression":
                    assert isinstance(value.expr.target, ExpressionId)

                    # find usages of this expression
                    usage_ids = usages.get(value.expr.target)
                    dataflows[node].uses.extend(usage_ids)

                # independently of the expression, this value also declares a variable
                vid = variables.get(node)
                dataflows[node].declares.append(vid)
                dataflows[flowgraph.exit].drops.append(vid)

    return OneToOne[FlowNode, DataFlow].instance(dataflows)
