from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
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
        views=GraphViews(list=ListAllExtractor),
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
        views=GraphViews(list=ListAcceptedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_flags_resolution(
    flags: OneToOne[FlagsId, Flags],
    registers: OneToOne[RegisterId, RegisterAcceptance],
) -> OneToOne[FlagsId, FlagsResolution]:
    resolutions: dict[FlagsId, FlagsResolution] = {}

    for fid, entry in flags.items():
        resolution = FlagsResolution(
            ref=entry.ref,
            id=fid,
            accepted=[],
            rejected=[],
        )

        names: set[bytes] = set()
        accepted: list[RegisterAcceptance] = []

        for id in entry.clobbers or []:
            register = registers.get(id)

            if register.name not in names:
                names.add(register.name)

            else:
                resolution.rejected.append(
                    FlagsRejection(
                        ref=register.ref,
                        id=fid,
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
    rule_e3002: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3002) == 0


def build_flags_resolution_accepted(
    resolutions: OneToOne[FlagsId, FlagsResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[FlagsId, FlagsAcceptance]:
    accepted: dict[FlagsId, FlagsAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[FlagsId, FlagsAcceptance].instance(accepted)


def validate_flags_resolution_e3002(
    flags: OneToOne[FlagsId, Flags],
    resolutions: OneToOne[FlagsId, FlagsResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

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


class ListAllExtractor:
    def __init__(self, data: OneToOne[FlagsId, FlagsResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[FlagsId, FlagsResolution]]:
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
    def rows(key: FlagsId, entry: FlagsResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[FlagsId, FlagsAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[FlagsId, FlagsAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "noreturn": "NoReturn",
            "clobbers": "Clobbers",
        }

    @staticmethod
    def rows(key: FlagsId, entry: FlagsAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "noreturn": str(entry.noreturn),
            "clobbers": ", ".join([clobber.name.decode() for clobber in entry.clobbers]),
        }
