from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.indices import Index, IndexId
from i13c.semantic.typing.entities.references import ReferenceId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.semantic.typing.resolutions.indices import (
    IndexAcceptance,
    IndexRejection,
    IndexResolution,
)
from i13c.semantic.typing.resolutions.parameters import ParameterAcceptance
from i13c.semantic.typing.resolutions.references import ReferenceAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance
from i13c.syntax.source import Span


def configure_index_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_index_resolution,
        constraint=None,
        produces=("resolutions/indices",),
        requires=frozenset(
            {
                ("indices", "entities/indices"),
                ("registers", "resolutions/registers/accepted"),
                ("references", "resolutions/references/accepted"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate_e3029 = GraphNode(
        builder=validate_index_resolution_e3029,
        constraint=None,
        produces=("rules/e3029",),
        requires=frozenset(
            {
                ("indices", "entities/indices"),
                ("resolutions", "resolutions/indices"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_index_resolution_accepted,
        constraint=check_index_resolution_accepted,
        produces=("resolutions/indices/accepted",),
        requires=frozenset(
            {
                ("rule_e3029", "rules/e3029"),
                ("resolutions", "resolutions/indices"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate_e3029, extract])


def build_index_resolution(
    indices: OneToOne[IndexId, Index],
    registers: OneToOne[RegisterId, RegisterAcceptance],
    references: OneToOne[ReferenceId, ReferenceAcceptance],
) -> OneToOne[IndexId, IndexResolution]:
    resolutions: dict[IndexId, IndexResolution] = {}

    for eid, entry in indices.items():
        resolution = IndexResolution(
            ref=entry.ref,
            id=eid,
            accepted=[],
            rejected=[],
        )

        # assume no displacement nor registers are available
        target: RegisterAcceptance | ParameterAcceptance | None = None

        match resolve_register(eid, entry.ref, entry.target, registers, references):
            case IndexRejection() as rejection:
                resolution.rejected.append(rejection)
            case RegisterAcceptance() as register:
                target = register
            case ParameterAcceptance() as register:
                target = register

        if isinstance(target, RegisterAcceptance):
            if target.name == b"rsp":  # noqa: SIM102
                resolution.rejected.append(
                    IndexRejection(
                        ref=entry.ref,
                        id=eid,
                        reason="invalid-register",
                    )
                )

        if entry.scale not in (1, 2, 4, 8):
            resolution.rejected.append(
                IndexRejection(
                    ref=entry.ref,
                    id=eid,
                    reason="invalid-scaler",
                )
            )

        elif len(resolution.rejected) == 0:
            assert target is not None

            resolution.accepted.append(
                IndexAcceptance(
                    ref=entry.ref,
                    id=eid,
                    scale=entry.scale,
                    target=target,
                )
            )

        resolutions[eid] = resolution

    return OneToOne[IndexId, IndexResolution].instance(resolutions)


def resolve_register(
    eid: IndexId,
    ref: Span,
    target: RegisterId | ReferenceId,
    registers: OneToOne[RegisterId, RegisterAcceptance],
    references: OneToOne[ReferenceId, ReferenceAcceptance],
) -> RegisterAcceptance | ParameterAcceptance | IndexRejection:

    if isinstance(target, RegisterId):
        register = registers.get(target)

        if register.kind != "64bit":
            return IndexRejection(
                ref=ref,
                id=eid,
                reason="invalid-register",
            )

        return register

    else:
        reference = references.get(target)

        if (
            not isinstance(reference.target, ParameterAcceptance)
            or reference.target.bind == "literal"
        ):
            return IndexRejection(
                ref=ref,
                id=eid,
                reason="invalid-register",
            )

        return reference.target


def check_index_resolution_accepted(
    rule_e3029: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3029) == 0


def build_index_resolution_accepted(
    resolutions: OneToOne[IndexId, IndexResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[IndexId, IndexAcceptance]:
    accepted: dict[IndexId, IndexAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[IndexId, IndexAcceptance].instance(accepted)


def validate_index_resolution_e3029(
    indices: OneToOne[IndexId, Index],
    resolutions: OneToOne[IndexId, IndexResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_index_resolution_e3029(indices.get(id), rejection)
                )

    return diagnostics


def report_index_resolution_e3029(
    entry: Index,
    rejection: IndexRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3029",
        message=f"Index resolution failed {entry!s}, reason: {rejection.reason}.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[IndexId, IndexResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[IndexId, IndexResolution]]:
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
    def rows(key: IndexId, entry: IndexResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[IndexId, IndexAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[IndexId, IndexAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "target": "Target",
        }

    @staticmethod
    def rows(key: IndexId, entry: IndexAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "target": entry.target.name.decode() if entry.target else "",
        }
