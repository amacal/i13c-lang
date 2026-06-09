from typing import Any, Dict, Iterable, List, Set, Tuple

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
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
        views=GraphViews(list=ListAllExtractor),
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
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_binding_resolution(
    signatures: OneToOne[SignatureId, SignatureAcceptance],
    binds: OneToOne[ParameterId, BindAcceptance],
) -> OneToOne[SignatureId, BindingResolution]:
    resolutions: Dict[SignatureId, BindingResolution] = {}

    for sid, entry in signatures.items():
        resolution = BindingResolution(
            ref=entry.ref,
            owner=sid,
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
                            owner=sid,
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


class ListAllExtractor:
    def __init__(self, data: OneToOne[SignatureId, BindingResolution]):
        self.data = data

    def extract(self) -> Iterable[Tuple[SignatureId, BindingResolution]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "sig": "Signature",
            "accepted": "Accepted",
            "rejected": "Rejected",
        }

    @staticmethod
    def rows(key: SignatureId, entry: BindingResolution) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "sig": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[SignatureId, BindingAcceptance]):
        self.data = data

    def extract(self) -> Iterable[Tuple[SignatureId, BindingAcceptance]]:
        for key, entry in self.data.items():
            yield key, entry

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "ref": "Ref",
            "sig": "Signature",
            "binds": "Binds",
        }

    @staticmethod
    def rows(key: SignatureId, entry: BindingAcceptance) -> Dict[str, str]:
        return {
            "ref": str(entry.ref),
            "sig": key.identify(1),
            "binds": str(len(entry.binds)),
        }
