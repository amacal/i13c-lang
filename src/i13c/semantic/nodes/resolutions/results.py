from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.results import Result, ResultId
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.resolutions.results import (
    ResultAcceptance,
    ResultResolution,
)
from i13c.semantic.typing.resolutions.types import TypeAcceptance


def configure_result_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_result_resolution,
        constraint=None,
        produces=("resolutions/results",),
        requires=frozenset(
            {
                ("results", "entities/results"),
                ("types", "resolutions/types/accepted"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_result_resolution_e3030,
        constraint=None,
        produces=("rules/e3030",),
        requires=frozenset(
            {
                ("results", "entities/results"),
                ("resolutions", "resolutions/results"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_result_resolution_accepted,
        constraint=check_result_resolution_accepted,
        produces=("resolutions/results/accepted",),
        requires=frozenset(
            {
                ("rule_e3030", "rules/e3030"),
                ("resolutions", "resolutions/results"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_result_resolution(
    results: OneToOne[ResultId, Result],
    types: OneToOne[TypeId, TypeAcceptance],
) -> OneToOne[ResultId, ResultResolution]:
    resolutions: dict[ResultId, ResultResolution] = {}

    for pid, entry in results.items():
        resolution = ResultResolution(
            ref=entry.ref,
            id=pid,
            accepted=[],
            rejected=[],
        )

        resolution.accepted.append(
            ResultAcceptance(
                ref=entry.ref,
                id=pid,
                type=types.get(entry.type),
            )
        )

        resolutions[pid] = resolution

    return OneToOne[ResultId, ResultResolution].instance(resolutions)


def check_result_resolution_accepted(
    rule_e3030: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3030) == 0


def build_result_resolution_accepted(
    resolutions: OneToOne[ResultId, ResultResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[ResultId, ResultAcceptance]:
    accepted: dict[ResultId, ResultAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[ResultId, ResultAcceptance].instance(accepted)


def validate_result_resolution_e3030(
    results: OneToOne[ResultId, Result],
    resolutions: OneToOne[ResultId, ResultResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(
                    report_result_resolution_e3030(results.get(id))
                )

    return diagnostics


def report_result_resolution_e3030(entry: Result) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3030",
        message=f"Invalid result {entry}, reason: unknown.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[ResultId, ResultResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[ResultId, ResultResolution]]:
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
    def rows(key: ResultId, entry: ResultResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[ResultId, ResultAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[ResultId, ResultAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "type": "Type",
            "width": "Width",
        }

    @staticmethod
    def rows(key: ResultId, entry: ResultAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "type": entry.type.name.decode(),
            "width": str(entry.type.width),
        }
