from collections.abc import Iterable

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
from i13c.semantic.typing.resolutions.literals import LiteralAcceptance
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
    dflows: dict[FunctionId, DataFlows] = {}

    for fid, entry in cflows.items():
        dflow = DataFlows(
            ref=entry.ref,
            target=fid,
            nodes=entry.nodes,
            values=[],
            forward={},
            backward={},
            defs={},
            uses={},
            clobbers={},
        )

        for idx, node in enumerate(entry.nodes):
            if idx == entry.entry:
                handle_entry(dflow, idx, functions.get(fid))

            elif isinstance(node, FlowNode):
                handle_node(dflow, idx, statements.get(node.target))

            else:
                dflow.defs[idx] = []
                dflow.uses[idx] = []

        dflows[fid] = dflow

    return OneToOne[FunctionId, DataFlows].instance(dflows)


def handle_entry(dflow: DataFlows, nid: int, target: FunctionAcceptance):
    dflow.defs[nid] = []
    dflow.uses[nid] = []

    for param in target.signature.parameters:
        idx = len(dflow.values)
        dflow.values.append(param)
        dflow.defs[nid].append(idx)
        dflow.forward[idx] = []
        dflow.backward[idx] = []


def handle_node(dflow: DataFlows, nid: int, stmt: StatementAcceptance):
    if isinstance(stmt.target, CallAcceptance):
        idx = len(dflow.values)
        dflow.values.append(stmt.target.target)
        dflow.defs[nid] = []
        dflow.uses[nid] = []
        dflow.forward[idx] = []
        dflow.backward[idx] = []
        dflow.clobbers[nid] = []

        for off, clobber in enumerate(stmt.target.target.clobbers):
            dflow.forward[idx + off + 1] = []
            dflow.backward[idx + off + 1] = []
            dflow.clobbers[nid].append(idx + off + 1)
            dflow.values.append(clobber)

        for arg in stmt.target.target.arguments:
            if isinstance(arg, ParameterAcceptance):
                for nix, node in enumerate(dflow.values):
                    if isinstance(node, ParameterAcceptance):  # noqa: SIM102
                        if node.id == arg.id:
                            dflow.forward[nix].append(idx)
                            dflow.backward[idx].append(nix)
                            dflow.uses[nid].append(nix)

            elif isinstance(arg, ValueAcceptance):
                for nix, node in enumerate(dflow.values):
                    if isinstance(node, ValueAcceptance):  # noqa: SIM102
                        if node.id == arg.id:
                            dflow.forward[nix].append(idx)
                            dflow.backward[idx].append(nix)
                            dflow.uses[nid].append(nix)

    if isinstance(stmt.target, AssignAcceptance):
        idx = len(dflow.values)
        dflow.values.append(stmt.target.destination)
        dflow.defs[nid] = [idx]
        dflow.uses[nid] = []
        dflow.forward[idx] = []
        dflow.backward[idx] = []

        if isinstance(stmt.target.expression, ExpressionAcceptance):
            for nix, node in enumerate(dflow.values):
                if isinstance(node, (ParameterAcceptance, ValueAcceptance)): # noqa: SIM102
                    if node.id == stmt.target.expression.target.id:
                        dflow.forward[nix].append(idx)
                        dflow.backward[idx].append(nix)
                        dflow.uses[nid].append(nix)

        # an assignment with literal makes short-lived inline edge
        if isinstance(stmt.target.expression, LiteralAcceptance):
            off = len(dflow.values)
            dflow.values.append(stmt.target.expression)
            dflow.forward[off] = [idx]
            dflow.backward[off] = []
            dflow.backward[idx].append(off)


class ListExtractor:
    def __init__(self, data: OneToOne[FunctionId, DataFlows]):
        self.data = data

    def extract(self) -> Iterable[tuple[FunctionId, DataFlows]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "values": "values",
            "forward": "Forward",
            "backward": "Backward",
        }

    @staticmethod
    def rows(key: FunctionId, entry: DataFlows) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "fn": key.identify(1),
            "values": str(len(entry.values)),
            "forward": str(len(entry.forward)),
            "backward": str(len(entry.backward)),
        }
