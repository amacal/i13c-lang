from typing import Any, Dict, List, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.parameters import ParameterId
from i13c.semantic.typing.entities.signatures import SignatureId
from i13c.semantic.typing.resolutions.bindings import (
    BindingAcceptance,
    BindingRejection,
    BindingResolution,
)
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.semantic.typing.resolutions.signatures import SignatureAcceptance


def configure_binding_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_binding_resolution,
        constraint=None,
        produces=("resolutions/bindings",),
        requires=frozenset(
            {
                ("signatures", "resolutions/signatures/accepted"),
                ("binds", "indices/binds/parameters"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_binding_resolution_e3011,
        constraint=None,
        produces=("rules/e3011",),
        requires=frozenset(
            {
                ("resolutions", "resolutions/bindings"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_binding_resolution_accepted,
        constraint=check_binding_resolution_accepted,
        produces=("resolutions/bindings/accepted",),
        requires=frozenset(
            {
                ("rule_e3011", "rules/e3011"),
                ("resolutions", "resolutions/bindings"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_binding_resolution(
    signatures: OneToOne[SignatureId, SignatureAcceptance],
    binds: OneToOne[ParameterId, BindAcceptance],
) -> OneToOne[SignatureId, BindingResolution]:
    resolutions: Dict[SignatureId, BindingResolution] = {}

    for sid, entry in signatures.items():
        resolution = BindingResolution(
            accepted=[],
            rejected=[],
        )

        names: Set[bytes] = set()
        found: List[BindAcceptance] = []

        # only snippets may have binds
        for parameter in entry.parameters:
            if bind := binds.find(parameter.id):
                if bind.mode == "register" and bind.dst in names:
                    resolution.rejected.append(
                        BindingRejection(
                            ref=bind.ref,
                            reason="duplicated-binds",
                        )
                    )

                else:
                    names.add(bind.dst)
                    found.append(bind)

        if len(resolution.rejected) == 0:
            resolution.accepted.append(
                BindingAcceptance(
                    ref=entry.ref,
                    owner=sid,
                    binds=found,
                )
            )

        resolutions[sid] = resolution

    return OneToOne[SignatureId, BindingResolution].instance(resolutions)


def check_binding_resolution_accepted(
    rule_e3011: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3011) == 0


def build_binding_resolution_accepted(
    resolutions: OneToOne[SignatureId, BindingResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[SignatureId, BindingAcceptance]:
    accepted: Dict[SignatureId, BindingAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[SignatureId, BindingAcceptance].instance(accepted)


def validate_binding_resolution_e3011(
    resolutions: OneToOne[SignatureId, BindingResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for _, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(report_binding_resolution_e3011(rejection))

    return diagnostics


def report_binding_resolution_e3011(
    rejection: BindingRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3011",
        message=f"Duplicated binding {rejection}.",
    )
