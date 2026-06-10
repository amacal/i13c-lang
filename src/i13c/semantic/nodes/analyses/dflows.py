from typing import Dict, Iterable, Tuple

from i13c.core.graph import GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.cflows import ControlFlows, FlowNode
from i13c.semantic.typing.analyses.dflows import DataFlows
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.assigns import AssignAcceptance
from i13c.semantic.typing.resolutions.calls import CallAcceptance
from i13c.semantic.typing.resolutions.expressions import ExpressionAcceptance
from i13c.semantic.typing.resolutions.functions import FunctionAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.statements import StatementAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance


def configure_data_flows() -> GraphNode:
    return GraphNode(
        builder=build_data_flows,
        constraint=None,
        produces=("analyses/dflows",),
        requires=frozenset(
            {
                ("cflows", "analyses/cflows"),
                ("functions", "resolutions/functions/accepted"),
                ("statements", "resolutions/statements/accepted"),
            }
        ),
        views=GraphViews(list=ListExtractor),
    )


def build_data_flows(
    cflows: OneToOne[FunctionId, ControlFlows],
    functions: OneToOne[FunctionId, FunctionAcceptance],
    statements: OneToOne[StatementId, StatementAcceptance],
) -> OneToOne[FunctionId, DataFlows]:
    dflows: Dict[FunctionId, DataFlows] = {}

    for fid, entry in cflows.items():
        dflow = DataFlows(
            ref=entry.ref,
            target=fid,
            nodes=[],
            forward={},
            backward={},
        )

        for idx, node in enumerate(entry.nodes):
            if idx == entry.entry:
                handle_entry(dflow, functions.get(fid))

            if isinstance(node, FlowNode):
                handle_node(dflow, statements.get(node.target))

        dflows[fid] = dflow

    return OneToOne[FunctionId, DataFlows].instance(dflows)


def handle_entry(dflow: DataFlows, target: FunctionAcceptance):
    for param in target.signature.parameters:
        idx = len(dflow.nodes)
        dflow.nodes.append(param)
        dflow.forward[idx] = []
        dflow.backward[idx] = []


def handle_node(dflow: DataFlows, stmt: StatementAcceptance):
    if isinstance(stmt.target, CallAcceptance):
        idx = len(dflow.nodes)
        dflow.nodes.append(stmt.target.target)
        dflow.forward[idx] = []
        dflow.backward[idx] = []

        for arg in stmt.target.target.arguments:
            if isinstance(arg, ParameterAcceptance):
                for nix, node in enumerate(dflow.nodes):
                    if isinstance(node, ParameterAcceptance):
                        if node.id == arg.id:
                            dflow.forward[nix].append(idx)
                            dflow.backward[idx].append(nix)

            elif isinstance(arg, ValueAcceptance):
                for nix, node in enumerate(dflow.nodes):
                    if isinstance(node, ValueAcceptance):
                        if node.id == arg.id:
                            dflow.forward[nix].append(idx)
                            dflow.backward[idx].append(nix)

    if isinstance(stmt.target, AssignAcceptance):
        idx = len(dflow.nodes)
        dflow.nodes.append(stmt.target.destination)
        dflow.forward[idx] = []
        dflow.backward[idx] = []

        if isinstance(stmt.target.expression, ExpressionAcceptance):
            for nix, node in enumerate(dflow.nodes):
                if isinstance(node, ParameterAcceptance):
                    if node.id == stmt.target.expression.target.id:
                        dflow.forward[nix].append(idx)
                        dflow.backward[idx].append(nix)

                elif isinstance(node, ValueAcceptance):
                    if node.id == stmt.target.expression.target.id:
                        dflow.forward[nix].append(idx)
                        dflow.backward[idx].append(nix)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, DataFlows]):
        self.data = data

    def extract(self) -> Iterable[Tuple[FunctionId, DataFlows]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "nodes": "Nodes",
            "forward": "Forward",
            "backward": "Backward",
        }

    @staticmethod
    def rows(key: FunctionId, entry: DataFlows) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "fn": key.identify(1),
            "nodes": str(len(entry.nodes)),
            "forward": str(len(entry.forward)),
            "backward": str(len(entry.backward)),
        }
