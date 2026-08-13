from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.references import Reference, ReferenceId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.environments import EnvironmentAcceptance
from i13c.semantic.typing.resolutions.labels import LabelAcceptance
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
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
        views=GraphViews(list=ListAllExtractor),
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
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate_e3020, extract])


def build_reference_resolution(
    references: OneToOne[ReferenceId, Reference],
    environments: OneToOne[SnippetId, EnvironmentAcceptance],
) -> OneToOne[ReferenceId, ReferenceResolution]:
    resolutions: dict[ReferenceId, ReferenceResolution] = {}

    for rid, entry in references.items():
        resolution = ReferenceResolution(
            ref=entry.ref,
            id=rid,
            accepted=[],
            rejected=[],
        )

        # find the environment of this reference
        snippet_id = entry.get_snippet(SnippetId.from_context)
        environment = environments.get(snippet_id)

        if entry.name not in environment.entries:
            resolution.rejected.append(
                ReferenceRejection(
                    ref=entry.ref,
                    id=rid,
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
    rule_e3020: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3020) == 0


def build_reference_resolution_accepted(
    resolutions: OneToOne[ReferenceId, ReferenceResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[ReferenceId, ReferenceAcceptance]:
    accepted: dict[ReferenceId, ReferenceAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[ReferenceId, ReferenceAcceptance].instance(accepted)


def validate_reference_resolution_e3020(
    references: OneToOne[ReferenceId, Reference],
    resolutions: OneToOne[ReferenceId, ReferenceResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

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


class ListAllExtractor:
    def __init__(self, data: OneToOne[ReferenceId, ReferenceResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[ReferenceId, ReferenceResolution]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "accepted": "Accepted",
            "rejected": "Rejected",
        }

    @staticmethod
    def rows(key: ReferenceId, entry: ReferenceResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[ReferenceId, ReferenceAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[ReferenceId, ReferenceAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "ptype": "Parameter Type",
            "pbind": "Parameter Bind",
            "lidx": "Label Index",
            "ltarget": "Label Target",
        }

    @staticmethod
    def rows(key: ReferenceId, entry: ReferenceAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "ptype": (
                str(entry.target.type.name)
                if isinstance(entry.target, ParameterAcceptance)
                else ""
            ),
            "pbind": (
                str(entry.target.bind)
                if isinstance(entry.target, ParameterAcceptance)
                else ""
            ),
            "lidx": (
                str(entry.target.index)
                if isinstance(entry.target, LabelAcceptance)
                else ""
            ),
            "ltarget": (
                entry.target.target.identify(1)
                if isinstance(entry.target, LabelAcceptance)
                else ""
            ),
        }
