from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.cflows import FunctionId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.entities.usages import Usage, UsageId
from i13c.semantic.typing.resolutions.cflows import ControlFlowAcceptance
from i13c.semantic.typing.resolutions.usages import (
    UsageAcceptance,
    UsageRejection,
    UsageResolution,
)


def configure_usage_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_usage_resolution,
        constraint=None,
        produces=("resolutions/usages",),
        requires=frozenset(
            {
                ("usages", "entities/usages"),
                ("cflows", "resolutions/cflows/accepted"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_usage_resolution_e3010,
        constraint=None,
        produces=("rules/e3010",),
        requires=frozenset(
            {
                ("usages", "entities/usages"),
                ("resolutions", "resolutions/usages"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_usage_resolution_accepted,
        constraint=check_usage_resolution_accepted,
        produces=("resolutions/usages/accepted",),
        requires=frozenset(
            {
                ("rule_e3010", "rules/e3010"),
                ("resolutions", "resolutions/usages"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_usage_resolution(
    usages: OneToOne[UsageId, Usage],
    cflows: OneToOne[FunctionId, ControlFlowAcceptance],
) -> OneToOne[UsageId, UsageResolution]:
    resolutions: dict[UsageId, UsageResolution] = {}

    for eid, entry in usages.items():
        resolution = UsageResolution(
            ref=entry.ref,
            id=eid,
            accepted=[],
            rejected=[],
        )

        # find components up in the hierarchy
        function_id = entry.get_function(FunctionId.from_context)
        statement_id = entry.get_statement(StatementId.from_context)

        # find related environment from control flow acceptance
        control_flow: ControlFlowAcceptance = cflows.get(function_id)
        environment = control_flow.environments[statement_id]

        if entry.name not in environment:
            resolution.rejected.append(
                UsageRejection(
                    ref=entry.ref,
                    id=eid,
                    name=entry.name,
                    reason="unresolved",
                )
            )

        if not resolution.rejected:
            resolution.accepted.append(
                UsageAcceptance(
                    ref=entry.ref,
                    id=eid,
                    name=entry.name,
                    target=environment[entry.name],
                    environment=environment,
                )
            )

        resolutions[eid] = resolution

    return OneToOne[UsageId, UsageResolution].instance(resolutions)


def check_usage_resolution_accepted(
    rule_e3010: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3010) == 0


def build_usage_resolution_accepted(
    resolutions: OneToOne[UsageId, UsageResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[UsageId, UsageAcceptance]:
    accepted: dict[UsageId, UsageAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[UsageId, UsageAcceptance].instance(accepted)


def validate_usage_resolution_e3010(
    usages: OneToOne[UsageId, Usage],
    resolutions: OneToOne[UsageId, UsageResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(
                    report_usage_resolution_e3010(usages.get(id))
                )

    return diagnostics


def report_usage_resolution_e3010(entry: Usage) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3010",
        message=f"Invalid usage {entry}, reason: unknown.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[UsageId, UsageResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[UsageId, UsageResolution]]:
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
    def rows(key: UsageId, entry: UsageResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[UsageId, UsageAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[UsageId, UsageAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "env": "Environment",
        }

    @staticmethod
    def rows(key: UsageId, entry: UsageAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "env": ", ".join(key.decode() for key in entry.environment),
        }
