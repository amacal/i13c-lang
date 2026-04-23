from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.cflows import (
    ControlFlows,
    FlowEntry,
    FlowExit,
    FlowNode,
)
from i13c.semantic.typing.entities.functions import Function, FunctionId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.cflows import (
    ControlFlowAcceptance,
    ControlFlowEntry,
    ControlFlowEnvironment,
    ControlFlowResolution,
)
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance
from i13c.semantic.typing.resolutions.values import ValueAcceptance


def configure_control_flow_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_control_flow_resolution,
        constraint=None,
        produces=("resolutions/cflows",),
        requires=frozenset(
            {
                ("cflows", "entities/cflows"),
                ("functions", "entities/functions"),
                ("values", "indices/values/statements"),
                ("signatures", "resolutions/signatures/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_control_flow_resolution_e3005,
        constraint=None,
        produces=("rules/e3005",),
        requires=frozenset(
            {
                ("cflows", "entities/cflows"),
                ("resolutions", "resolutions/cflows"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_control_flow_resolution_accepted,
        constraint=check_control_flow_resolution_accepted,
        produces=("resolutions/cflows/accepted",),
        requires=frozenset(
            {
                ("rule_e3005", "rules/e3005"),
                ("resolutions", "resolutions/cflows"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_control_flow_resolution(
    cflows: OneToOne[FunctionId, ControlFlows],
    functions: OneToOne[FunctionId, Function],
    values: OneToMany[StatementId, ValueAcceptance],
    signatures: OneToOne[SignatureId, SignatureAcceptance],
) -> OneToOne[FunctionId, ControlFlowResolution]:
    resolutions: Dict[FunctionId, ControlFlowResolution] = {}

    for fid, entry in cflows.items():
        resolution = ControlFlowResolution(
            accepted=[],
            rejected=[],
        )

        assert isinstance(entry.nodes[0], FlowEntry)
        fentry: FlowEntry = entry.nodes[0]

        assert isinstance(entry.nodes[-1], FlowExit)
        fexit: FlowExit = entry.nodes[-1]

        function = functions.get(fid)
        signature = signatures.get(function.signature)

        next: ControlFlowEntry = {}
        environments: ControlFlowEnvironment = {
            fentry: {},
        }

        for param in signature.parameters:
            next[param.name] = param

        for node in entry.nodes[1:-1]:
            assert isinstance(node, FlowNode)

            # previous entries have to be copied to the new node
            environments[node.target] = next.copy()

            # assignment causes new entry in the environment
            for value in values.find(node.target):
                next[value.name] = value

        environments[fexit] = next.copy()

        resolution.accepted.append(
            ControlFlowAcceptance(
                ref=entry.ref,
                id=fid,
                entry=fentry,
                exit=fexit,
                environments=environments,
            )
        )

        resolutions[fid] = resolution

    return OneToOne[FunctionId, ControlFlowResolution].instance(resolutions)


def check_control_flow_resolution_accepted(
    rule_e3005: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3005) == 0


def build_control_flow_resolution_accepted(
    resolutions: OneToOne[FunctionId, ControlFlowResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[FunctionId, ControlFlowAcceptance]:
    accepted: Dict[FunctionId, ControlFlowAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[FunctionId, ControlFlowAcceptance].instance(accepted)


def validate_control_flow_resolution_e3005(
    cflows: OneToOne[FunctionId, ControlFlows],
    resolutions: OneToOne[FunctionId, ControlFlowResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(
                    report_control_flow_resolution_e3005(cflows.get(id)),
                )

    return diagnostics


def report_control_flow_resolution_e3005(entry: ControlFlows) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3005",
        message=f"Invalid control flow {entry}, reason: unknown.",
    )
