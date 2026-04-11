from typing import Any, Dict, List, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.binds import Bind, BindId
from i13c.semantic.typing.resolutions.binds import (
    BindAcceptance,
    BindRejection,
    BindResolution,
)


def configure_bind_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_bind_resolution,
        constraint=None,
        produces=("resolutions/binds",),
        requires=frozenset({("binds", "entities/binds")}),
    )

    validate = GraphNode(
        builder=validate_bind_resolution_e3013,
        constraint=None,
        produces=("rules/e3013",),
        requires=frozenset(
            {
                ("binds", "entities/binds"),
                ("resolutions", "resolutions/binds"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_bind_resolution_accepted,
        constraint=check_bind_resolution_accepted,
        produces=("resolutions/binds/accepted",),
        requires=frozenset(
            {
                ("rule_e3013", "rules/e3013"),
                ("resolutions", "resolutions/binds"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_bind_resolution(
    binds: OneToOne[BindId, Bind],
) -> OneToOne[BindId, BindResolution]:
    resolutions: Dict[BindId, BindResolution] = {}

    # fmt: off
    whitelist: Set[bytes] = set([
        b"rax", b"rbx", b"rcx", b"rdx", b"rsi", b"rdi", b"rsp", b"rbp",
        b"r8", b"r9", b"r10", b"r11", b"r12", b"r13", b"r14", b"r15", b"imm",
    ])
    # fmt: on

    for bid, entry in binds.items():
        resolution = BindResolution(
            accepted=[],
            rejected=[],
        )

        if entry.name not in whitelist:
            resolution.rejected.append(
                BindRejection(
                    ref=entry.ref,
                    reason="unknown-register",
                )
            )

        else:
            resolution.accepted.append(
                BindAcceptance(
                    ref=entry.ref,
                    id=bid,
                    target=entry.name,
                    mode="immediate" if entry.name == b"imm" else "register",
                )
            )

        resolutions[bid] = resolution

    return OneToOne[BindId, BindResolution].instance(resolutions)


def check_bind_resolution_accepted(
    rule_e3013: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3013) == 0


def build_bind_resolution_accepted(
    resolutions: OneToOne[BindId, BindResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[BindId, BindAcceptance]:
    accepted: Dict[BindId, BindAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[BindId, BindAcceptance].instance(accepted)


def validate_bind_resolution_e3013(
    binds: OneToOne[BindId, Bind],
    resolutions: OneToOne[BindId, BindResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_bind_resolution_e3013(binds.get(id), rejection)
                )

    return diagnostics


def report_bind_resolution_e3013(entry: Bind, rejection: BindRejection) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3013",
        message=f"Invalid slot bind {entry}, reason: {rejection.reason}.",
    )
