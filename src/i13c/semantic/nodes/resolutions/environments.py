from typing import Any, Dict, List, Sequence

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.environments import Environment, EnvironmentId
from i13c.semantic.typing.entities.labels import LabelId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.environments import (
    EnvironmentAcceptance,
    EnvironmentRejection,
    EnvironmentResolution,
    EnvironmentTarget,
)
from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance


def configure_environment_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_environment_resolution,
        constraint=None,
        produces=("resolutions/environments",),
        requires=frozenset(
            {
                ("environments", "entities/environments"),
                ("labels", "resolutions/labels/accepted"),
                ("signatures", "resolutions/signatures/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_environment_resolution_e3019,
        constraint=None,
        produces=("rules/e3019",),
        requires=frozenset(
            {
                ("environments", "entities/environments"),
                ("resolutions", "resolutions/environments"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_environment_resolution_accepted,
        constraint=check_environment_resolution_accepted,
        produces=("resolutions/environments/accepted",),
        requires=frozenset(
            {
                ("rule_e3019", "rules/e3019"),
                ("resolutions", "resolutions/environments"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_environment_resolution(
    environments: OneToOne[EnvironmentId, Environment],
    labels: OneToOne[LabelId, LabelAcceptance],
    signatures: OneToOne[SignatureId, SignatureAcceptance],
) -> OneToOne[EnvironmentId, EnvironmentResolution]:
    resolutions: Dict[EnvironmentId, EnvironmentResolution] = {}

    for eid, entry in environments.items():
        resolution = EnvironmentResolution(
            accepted=[],
            rejected=[],
        )

        mapping: Dict[bytes, EnvironmentTarget] = {}

        for item in entry.entries:
            targets: Sequence[EnvironmentTarget]

            if isinstance(item, SignatureId):
                targets = signatures.get(item).slots
            else:
                targets = [labels.get(item)]

            for target in targets:
                if target.name not in mapping:
                    mapping[target.name] = target
                else:
                    resolution.rejected.append(
                        EnvironmentRejection(
                            ref=target.ref,
                            reason="duplicated-name",
                        )
                    )

        if not resolution.rejected:
            resolution.accepted.append(
                EnvironmentAcceptance(
                    ref=entry.ref,
                    id=eid,
                    ctx=entry.ctx,
                    kind=entry.kind,
                    entries=mapping,
                )
            )

        resolutions[eid] = resolution

    return OneToOne[EnvironmentId, EnvironmentResolution].instance(resolutions)


def check_environment_resolution_accepted(
    rule_e3019: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3019) == 0


def build_environment_resolution_accepted(
    resolutions: OneToOne[EnvironmentId, EnvironmentResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[EnvironmentId, EnvironmentAcceptance]:
    accepted: Dict[EnvironmentId, EnvironmentAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[EnvironmentId, EnvironmentAcceptance].instance(accepted)


def validate_environment_resolution_e3019(
    environments: OneToOne[EnvironmentId, Environment],
    resolutions: OneToOne[EnvironmentId, EnvironmentResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_environment_resolution_e3019(environments.get(id), rejection)
                )

    return diagnostics


def report_environment_resolution_e3019(
    entry: Environment, rejection: EnvironmentRejection
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3019",
        message=f"Invalid environment {entry}, reason: {rejection.reason}.",
    )
