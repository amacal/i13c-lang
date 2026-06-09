from typing import Any, Dict, Iterable, List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.entities.values import Value, ValueId
from i13c.semantic.typing.resolutions.types import TypeAcceptance
from i13c.semantic.typing.resolutions.values import (
    ValueAcceptance,
    ValueResolution,
)


def configure_value_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_value_resolution,
        constraint=None,
        produces=("resolutions/values",),
        requires=frozenset(
            {
                ("values", "entities/values"),
                ("types", "resolutions/types/accepted"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_value_resolution_e3008,
        constraint=None,
        produces=("rules/e3008",),
        requires=frozenset(
            {
                ("values", "entities/values"),
                ("resolutions", "resolutions/values"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_value_resolution_accepted,
        constraint=check_value_resolution_accepted,
        produces=("resolutions/values/accepted",),
        requires=frozenset(
            {
                ("rule_e3008", "rules/e3008"),
                ("resolutions", "resolutions/values"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_value_resolution(
    values: OneToOne[ValueId, Value],
    types: OneToOne[TypeId, TypeAcceptance],
) -> OneToOne[ValueId, ValueResolution]:
    resolutions: Dict[ValueId, ValueResolution] = {}

    for vid, entry in values.items():
        resolution = ValueResolution(
            ref=entry.ref,
            id=vid,
            accepted=[],
            rejected=[],
        )

        resolution.accepted.append(
            ValueAcceptance(
                ref=entry.ref,
                id=vid,
                stmt=entry.stmt,
                name=entry.name,
                type=types.get(entry.type),
            )
        )

        resolutions[vid] = resolution

    return OneToOne[ValueId, ValueResolution].instance(resolutions)


def check_value_resolution_accepted(
    rule_e3008: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3008) == 0


def build_value_resolution_accepted(
    resolutions: OneToOne[ValueId, ValueResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[ValueId, ValueAcceptance]:
    accepted: Dict[ValueId, ValueAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[ValueId, ValueAcceptance].instance(accepted)


def validate_value_resolution_e3008(
    values: OneToOne[ValueId, Value],
    resolutions: OneToOne[ValueId, ValueResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(report_value_resolution_e3008(values.get(id)))

    return diagnostics


def report_value_resolution_e3008(entry: Value) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3008",
        message=f"Invalid value {entry}, reason: unknown.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[ValueId, ValueResolution]):
        self.data = data

    def extract(self) -> Iterable[Tuple[ValueId, ValueResolution]]:
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
    def rows(key: ValueId, entry: ValueResolution) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[ValueId, ValueAcceptance]):
        self.data = data

    def extract(self) -> Iterable[Tuple[ValueId, ValueAcceptance]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "type": "Type",
        }

    @staticmethod
    def rows(key: ValueId, entry: ValueAcceptance) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "type": str(entry.type),

        }
