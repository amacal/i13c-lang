from typing import Any, Dict, Iterable, List, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.labels import Label, LabelId
from i13c.semantic.typing.resolutions.labels import LabelAcceptance, LabelResolution


def configure_label_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_label_resolution,
        constraint=None,
        produces=("resolutions/labels",),
        requires=frozenset(
            {
                ("labels", "entities/labels"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_label_resolution_e3018,
        constraint=None,
        produces=("rules/e3018",),
        requires=frozenset(
            {
                ("labels", "entities/labels"),
                ("resolutions", "resolutions/labels"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_label_resolution_accepted,
        constraint=check_label_resolution_accepted,
        produces=("resolutions/labels/accepted",),
        requires=frozenset(
            {
                ("rule_e3018", "rules/e3018"),
                ("resolutions", "resolutions/labels"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_label_resolution(
    labels: OneToOne[LabelId, Label],
) -> OneToOne[LabelId, LabelResolution]:
    resolutions: Dict[LabelId, LabelResolution] = {}

    for lid, entry in labels.items():
        resolution = LabelResolution(
            ref=entry.ref,
            id=lid,
            accepted=[],
            rejected=[],
        )

        resolution.accepted.append(
            LabelAcceptance(
                ref=entry.ref,
                id=lid,
                index=entry.index,
                name=entry.name,
                target=entry.target,
            )
        )

        resolutions[lid] = resolution

    return OneToOne[LabelId, LabelResolution].instance(resolutions)


def check_label_resolution_accepted(
    rule_e3018: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3018) == 0


def build_label_resolution_accepted(
    resolutions: OneToOne[LabelId, LabelResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[LabelId, LabelAcceptance]:
    accepted: Dict[LabelId, LabelAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[LabelId, LabelAcceptance].instance(accepted)


def validate_label_resolution_e3018(
    labels: OneToOne[LabelId, Label],
    resolutions: OneToOne[LabelId, LabelResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(report_label_resolution_e3018(labels.get(id)))

    return diagnostics


def report_label_resolution_e3018(entry: Label) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3018",
        message=f"Invalid label {entry}, reason: unknown.",
    )


class ListAllExtractor:
    def __init__(self, data: OneToOne[LabelId, LabelResolution]):
        self.data = data

    def extract(self) -> Iterable[Tuple[LabelId, LabelResolution]]:
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
    def rows(key: LabelId, entry: LabelResolution) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[LabelId, LabelAcceptance]):
        self.data = data

    def extract(self) -> Iterable[Tuple[LabelId, LabelAcceptance]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "idx": "Index",
            "name": "Name",
            "target": "Target",
        }

    @staticmethod
    def rows(key: LabelId, entry: LabelAcceptance) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "idx": str(entry.index),
            "name": entry.name.decode(),
            "target": entry.target.identify(1),
        }
