from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.calls import Call, CallId
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.resolutions.calls import CallAcceptance, CallResolution
from i13c.semantic.typing.resolutions.callsites import CallSiteAcceptance


def configure_call_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_call_resolution,
        constraint=None,
        produces=("resolutions/calls",),
        requires=frozenset(
            {
                ("calls", "entities/calls"),
                ("callsites", "resolutions/callsites/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_call_resolution_e3025,
        constraint=None,
        produces=("rules/e3025",),
        requires=frozenset(
            {
                ("calls", "entities/calls"),
                ("resolutions", "resolutions/calls"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_call_resolution_accepted,
        constraint=check_call_resolution_accepted,
        produces=("resolutions/calls/accepted",),
        requires=frozenset(
            {
                ("rule_e3025", "rules/e3025"),
                ("resolutions", "resolutions/calls"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_call_resolution(
    calls: OneToOne[CallId, Call],
    callsites: OneToOne[CallSiteId, CallSiteAcceptance],
) -> OneToOne[CallId, CallResolution]:
    resolutions: Dict[CallId, CallResolution] = {}

    for cid, entry in calls.items():
        resolution = CallResolution(
            accepted=[],
            rejected=[],
        )

        resolution.accepted.append(
            CallAcceptance(
                ref=entry.ref,
                id=cid,
                target=callsites.get(entry.target),
            )
        )

        resolutions[cid] = resolution

    return OneToOne[CallId, CallResolution].instance(resolutions)


def check_call_resolution_accepted(
    rule_e3025: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3025) == 0


def build_call_resolution_accepted(
    resolutions: OneToOne[CallId, CallResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[CallId, CallAcceptance]:
    accepted: Dict[CallId, CallAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[CallId, CallAcceptance].instance(accepted)


def validate_call_resolution_e3025(
    calls: OneToOne[CallId, Call],
    resolutions: OneToOne[CallId, CallResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(report_call_resolution_e3025(calls.get(id)))

    return diagnostics


def report_call_resolution_e3025(entry: Call) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3025",
        message=f"Invalid call {entry}, reason: unknown.",
    )
