from typing import Any, Dict, List, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.flags import Flags, FlagsId
from i13c.semantic.typing.entities.registers import RegisterId
from i13c.semantic.typing.resolutions.flags import (
    FlagsAcceptance,
    FlagsRejection,
    FlagsResolution,
)
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance


def configure_flags_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_flags_resolution,
        constraint=None,
        produces=("resolutions/flags",),
        requires=frozenset(
            {
                ("flags", "entities/flags"),
                ("registers", "resolutions/registers/accepted"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_flags_resolution_e3002,
        constraint=None,
        produces=("rules/e3002",),
        requires=frozenset(
            {
                ("flags", "entities/flags"),
                ("resolutions", "resolutions/flags"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_flags_resolution_accepted,
        constraint=check_flags_resolution_accepted,
        produces=("resolutions/flags/accepted",),
        requires=frozenset(
            {
                ("rule_e3002", "rules/e3002"),
                ("resolutions", "resolutions/flags"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_flags_resolution(
    flags: OneToOne[FlagsId, Flags],
    registers: OneToOne[RegisterId, RegisterAcceptance],
) -> OneToOne[FlagsId, FlagsResolution]:
    resolutions: Dict[FlagsId, FlagsResolution] = {}

    for fid, entry in flags.items():
        resolution = FlagsResolution(
            accepted=[],
            rejected=[],
        )

        names: Set[bytes] = set()
        accepted: List[RegisterAcceptance] = []

        for id in entry.clobbers or []:
            register = registers.get(id)

            if register.name not in names:
                names.add(register.name)

            else:
                resolution.rejected.append(
                    FlagsRejection(
                        ref=register.ref,
                        reason="duplicated-register",
                    )
                )

            # the register survived the checks
            accepted.append(register)

        if len(resolution.rejected) == 0:
            resolution.accepted.append(
                FlagsAcceptance(
                    ref=entry.ref,
                    id=fid,
                    clobbers=accepted,
                    noreturn=entry.noreturn or False,
                )
            )

        resolutions[fid] = resolution

    return OneToOne[FlagsId, FlagsResolution].instance(resolutions)


def check_flags_resolution_accepted(
    rule_e3002: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3002) == 0


def build_flags_resolution_accepted(
    resolutions: OneToOne[FlagsId, FlagsResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[FlagsId, FlagsAcceptance]:
    accepted: Dict[FlagsId, FlagsAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[FlagsId, FlagsAcceptance].instance(accepted)


def validate_flags_resolution_e3002(
    flags: OneToOne[FlagsId, Flags],
    resolutions: OneToOne[FlagsId, FlagsResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                if rejection.reason == "duplicated-register":
                    diagnostics.append(
                        report_flags_resolution_e3002(flags.get(id), rejection)
                    )

    return diagnostics


def report_flags_resolution_e3002(
    entry: Flags,
    rejection: FlagsRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3002",
        message=f"Duplicated register name {entry}.",
    )
