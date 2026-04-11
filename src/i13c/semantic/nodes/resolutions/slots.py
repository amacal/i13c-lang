from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.binds import BindId
from i13c.semantic.typing.entities.slots import Slot, SlotId
from i13c.semantic.typing.entities.types import TypeId
from i13c.semantic.typing.resolutions.binds import BindAcceptance
from i13c.semantic.typing.resolutions.slots import SlotAcceptance, SlotResolution
from i13c.semantic.typing.resolutions.types import TypeAcceptance


def configure_slot_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_slot_resolution,
        constraint=None,
        produces=("resolutions/slots",),
        requires=frozenset(
            {
                ("slots", "entities/slots"),
                ("types", "resolutions/types/accepted"),
                ("binds", "resolutions/binds/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_slot_resolution_e3014,
        constraint=None,
        produces=("rules/e3014",),
        requires=frozenset(
            {
                ("slots", "entities/slots"),
                ("resolutions", "resolutions/slots"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_slot_resolution_accepted,
        constraint=check_slot_resolution_accepted,
        produces=("resolutions/slots/accepted",),
        requires=frozenset(
            {
                ("rule_e3014", "rules/e3014"),
                ("resolutions", "resolutions/slots"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_slot_resolution(
    slots: OneToOne[SlotId, Slot],
    types: OneToOne[TypeId, TypeAcceptance],
    binds: OneToOne[BindId, BindAcceptance],
) -> OneToOne[SlotId, SlotResolution]:
    resolutions: Dict[SlotId, SlotResolution] = {}

    for sid, entry in slots.items():
        resolution = SlotResolution(
            accepted=[],
            rejected=[],
        )

        resolution.accepted.append(
            SlotAcceptance(
                ref=entry.ref,
                id=sid,
                name=entry.name,
                bind=binds.get(slots.get(sid).bind),
                type=types.get(slots.get(sid).type),
            )
        )

        resolutions[sid] = resolution

    return OneToOne[SlotId, SlotResolution].instance(resolutions)


def check_slot_resolution_accepted(
    rule_e3014: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3014) == 0


def build_slot_resolution_accepted(
    resolutions: OneToOne[SlotId, SlotResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[SlotId, SlotAcceptance]:
    accepted: Dict[SlotId, SlotAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[SlotId, SlotAcceptance].instance(accepted)


def validate_slot_resolution_e3014(
    slots: OneToOne[SlotId, Slot],
    resolutions: OneToOne[SlotId, SlotResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for _ in resolution.rejected:
                diagnostics.append(report_slot_resolution_e3014(slots.get(id)))

    return diagnostics


def report_slot_resolution_e3014(entry: Slot) -> Diagnostic:
    return Diagnostic(
        ref=entry.ref,
        code="E3014",
        message=f"Invalid slot {entry}, reason: unknown.",
    )
