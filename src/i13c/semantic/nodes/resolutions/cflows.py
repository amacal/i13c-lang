from typing import Any, Dict, Iterable, List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.analyses.cflows import (
    ControlFlows,
    FlowEntry,
    FlowExit,
    FlowMember,
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
                ("cflows", "analyses/cflows"),
                ("functions", "entities/functions"),
                ("values", "indices/values/statements"),
                ("signatures", "resolutions/signatures/accepted"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_control_flow_resolution_e3005,
        constraint=None,
        produces=("rules/e3005",),
        requires=frozenset(
            {
                ("cflows", "analyses/cflows"),
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
        views=GraphViews(list=ListAcceptedExtractor),
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
        function = functions.get(fid)
        signature = signatures.get(function.signature)

        resolution = ControlFlowResolution(
            ref=entry.ref,
            function=fid,
            signature=function.signature,
            accepted=[],
            rejected=[],
        )

        fentry: FlowMember = entry.nodes[entry.entry]
        assert isinstance(fentry, FlowEntry)

        fexit: FlowMember = entry.nodes[entry.exit]
        assert isinstance(fexit, FlowExit)

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
                source=entry,
                function=fid,
                signature=function.signature,
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


class ListAllExtractor:
    def __init__(self, data: OneToOne[FunctionId, ControlFlowResolution]):
        self.data = data

    def extract(self) -> Iterable[Tuple[FunctionId, ControlFlowResolution]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "sig": "Signature",
            "accepted": "Accepted",
            "rejected": "Rejected",
        }

    @staticmethod
    def rows(key: FunctionId, entry: ControlFlowResolution) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "fn": key.identify(1),
            "sig": entry.signature.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[FunctionId, ControlFlowAcceptance]):
        self.data = data

    def extract(self) -> Iterable[Tuple[FunctionId, ControlFlowAcceptance]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "fn": "Function",
            "sig": "Signature",
            "envs": "Environments",
        }

    @staticmethod
    def rows(key: FunctionId, entry: ControlFlowAcceptance) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "fn": key.identify(1),
            "sig": entry.signature.identify(1),
            "envs": str(len(entry.environments)),
        }
