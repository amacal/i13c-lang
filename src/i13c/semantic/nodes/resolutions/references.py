from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.references import Reference, ReferenceId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.environments import EnvironmentAcceptance
from i13c.semantic.typing.resolutions.references import (
    ReferenceAcceptance,
    ReferenceRejection,
    ReferenceResolution,
)


def configure_reference_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_reference_resolution,
        constraint=None,
        produces=("resolutions/references",),
        requires=frozenset(
            {
                ("references", "entities/references"),
                ("environments", "indices/environments/snippets"),
            }
        ),
    )

    validate_e3020 = GraphNode(
        builder=validate_reference_resolution_e3020,
        constraint=None,
        produces=("rules/e3020",),
        requires=frozenset(
            {
                ("references", "entities/references"),
                ("resolutions", "resolutions/references"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_reference_resolution_accepted,
        constraint=check_reference_resolution_accepted,
        produces=("resolutions/references/accepted",),
        requires=frozenset(
            {
                ("rule_e3020", "rules/e3020"),
                ("resolutions", "resolutions/references"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate_e3020, extract])


def build_reference_resolution(
    references: OneToOne[ReferenceId, Reference],
    environments: OneToOne[SnippetId, EnvironmentAcceptance],
) -> OneToOne[ReferenceId, ReferenceResolution]:
    resolutions: Dict[ReferenceId, ReferenceResolution] = {}

    for rid, entry in references.items():
        resolution = ReferenceResolution(
            accepted=[],
            rejected=[],
        )

        # find the environment of this reference
        environment = environments.get(entry.ctx)

        if entry.name not in environment.entries:
            resolution.rejected.append(
                ReferenceRejection(
                    ref=entry.ref,
                    name=entry.name,
                    reason="unknown-name",
                )
            )

        else:
            resolution.accepted.append(
                ReferenceAcceptance(
                    ref=entry.ref,
                    id=rid,
                    name=entry.name,
                    target=environment.entries[entry.name],
                )
            )

        resolutions[rid] = resolution

    return OneToOne[ReferenceId, ReferenceResolution].instance(resolutions)


def check_reference_resolution_accepted(
    rule_e3020: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3020) == 0


def build_reference_resolution_accepted(
    resolutions: OneToOne[ReferenceId, ReferenceResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[ReferenceId, ReferenceAcceptance]:
    accepted: Dict[ReferenceId, ReferenceAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[ReferenceId, ReferenceAcceptance].instance(accepted)


def validate_reference_resolution_e3020(
    references: OneToOne[ReferenceId, Reference],
    resolutions: OneToOne[ReferenceId, ReferenceResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_reference_resolution_e3020(references.get(id), rejection)
                )

    return diagnostics


def report_reference_resolution_e3020(
    entry: Reference,
    rejection: ReferenceRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3020",
        message=f"Reference resolution failed {entry.name.decode()}, reason: {rejection.reason}.",
    )
