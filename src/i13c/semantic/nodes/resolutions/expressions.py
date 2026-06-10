from typing import Any, Dict, Iterable, List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.analyses.cflows import FunctionId
from i13c.semantic.typing.entities.expressions import Expression, ExpressionId
from i13c.semantic.typing.entities.statements import StatementId
from i13c.semantic.typing.resolutions.cflows import ControlFlowAcceptance
from i13c.semantic.typing.resolutions.expressions import (
    ExpressionAcceptance,
    ExpressionRejection,
    ExpressionResolution,
)


def configure_expression_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_expression_resolution,
        constraint=None,
        produces=("resolutions/expressions",),
        requires=frozenset(
            {
                ("expressions", "entities/expressions"),
                ("cflows", "resolutions/cflows/accepted"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_expression_resolution_e3010,
        constraint=None,
        produces=("rules/e3010",),
        requires=frozenset(
            {
                ("expressions", "entities/expressions"),
                ("resolutions", "resolutions/expressions"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_expression_resolution_accepted,
        constraint=check_expression_resolution_accepted,
        produces=("resolutions/expressions/accepted",),
        requires=frozenset(
            {
                ("rule_e3010", "rules/e3010"),
                ("resolutions", "resolutions/expressions"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_expression_resolution(
    expressions: OneToOne[ExpressionId, Expression],
    cflows: OneToOne[FunctionId, ControlFlowAcceptance],
) -> OneToOne[ExpressionId, ExpressionResolution]:
    resolutions: Dict[ExpressionId, ExpressionResolution] = {}

    for eid, entry in expressions.items():
        resolution = ExpressionResolution(
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
                ExpressionRejection(
                    ref=entry.ref,
                    id=eid,
                    name=entry.name,
                    reason="unresolved",
                )
            )

        if not resolution.rejected:
            resolution.accepted.append(
                ExpressionAcceptance(
                    ref=entry.ref,
                    id=eid,
                    name=entry.name,
                    target=environment[entry.name],
                    environment=environment,
                )
            )

        resolutions[eid] = resolution

    return OneToOne[ExpressionId, ExpressionResolution].instance(resolutions)


def check_expression_resolution_accepted(
    rule_e3010: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3010) == 0


def build_expression_resolution_accepted(
    resolutions: OneToOne[ExpressionId, ExpressionResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[ExpressionId, ExpressionAcceptance]:
    accepted: Dict[ExpressionId, ExpressionAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[ExpressionId, ExpressionAcceptance].instance(accepted)


def validate_expression_resolution_e3010(
    expressions: OneToOne[ExpressionId, Expression],
    resolutions: OneToOne[ExpressionId, ExpressionResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(
                    report_expression_resolution_e3010(expressions.get(id))
                )

    return diagnostics


def report_expression_resolution_e3010(entry: Expression) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3010",
        message=f"Invalid expression {entry}, reason: unknown.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[ExpressionId, ExpressionResolution]):
        self.data = data

    def extract(self) -> Iterable[Tuple[ExpressionId, ExpressionResolution]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "accepted": "Accepted",
            "rejected": "Rejected",
        }

    @staticmethod
    def rows(key: ExpressionId, entry: ExpressionResolution) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[ExpressionId, ExpressionAcceptance]):
        self.data = data

    def extract(self) -> Iterable[Tuple[ExpressionId, ExpressionAcceptance]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "env": "Environment",
        }

    @staticmethod
    def rows(key: ExpressionId, entry: ExpressionAcceptance) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "env": ", ".join(key.decode() for key in entry.environment.keys()),
        }
