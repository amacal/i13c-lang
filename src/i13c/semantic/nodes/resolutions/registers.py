from typing import Any, Dict, List, Set

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.registers import Register, RegisterId
from i13c.semantic.typing.resolutions.registers import (
    RegisterAcceptance,
    RegisterKind,
    RegisterRejection,
    RegisterResolution,
    RegisterWidth,
)


def configure_register_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_register_resolution,
        constraint=None,
        produces=("resolutions/registers",),
        requires=frozenset(
            {
                ("registers", "entities/registers"),
            }
        ),
    )

    validate = GraphNode(
        builder=validate_register_resolution_e3017,
        constraint=None,
        produces=("rules/e3017",),
        requires=frozenset(
            {
                ("registers", "entities/registers"),
                ("resolutions", "resolutions/registers"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_register_resolution_accepted,
        constraint=check_register_resolution_accepted,
        produces=("resolutions/registers/accepted",),
        requires=frozenset(
            {
                ("rule_e3017", "rules/e3017"),
                ("resolutions", "resolutions/registers"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_register_resolution(
    registers: OneToOne[RegisterId, Register],
) -> OneToOne[RegisterId, RegisterResolution]:
    resolutions: Dict[RegisterId, RegisterResolution] = {}

    # fmt: off
    widths: Dict[RegisterWidth, Set[bytes]] = {
        8: { b"al", b"cl", b"dl", b"bl", b"ah", b"ch", b"dh", b"bh", b"spl", b"bpl", b"sil", b"dil", b"r8b", b"r9b", b"r10b", b"r11b", b"r12b", b"r13b", b"r14b", b"r15b" },
        16: { b"ax", b"cx", b"dx", b"bx", b"sp", b"bp", b"si", b"di", b"r8w", b"r9w", b"r10w", b"r11w", b"r12w", b"r13w", b"r14w", b"r15w" },
        32: { b"eax", b"ecx", b"edx", b"ebx", b"esp", b"ebp", b"esi", b"edi", b"r8d", b"r9d", b"r10d", b"r11d", b"r12d", b"r13d", b"r14d", b"r15d" },
        64: { b"rax", b"rcx", b"rdx", b"rbx", b"rsp", b"rbp", b"rsi", b"rdi", b"r8", b"r9", b"r10", b"r11", b"r12", b"r13", b"r14", b"r15", b"rip" },
    }

    kinds: Dict[RegisterKind, Set[bytes]] = {
        "rip": { b"rip" },
        "low": { b"al", b"cl", b"dl", b"bl" },
        "high": { b"ah", b"ch", b"dh", b"bh" },
        "8bit": { b"spl", b"bpl", b"sil", b"dil", b"r8b", b"r9b", b"r10b", b"r11b", b"r12b", b"r13b", b"r14b", b"r15b" },
        "16bit": { b"ax", b"cx", b"dx", b"bx", b"sp", b"bp", b"si", b"di", b"r8w", b"r9w", b"r10w", b"r11w", b"r12w", b"r13w", b"r14w", b"r15w" },
        "32bit": { b"eax", b"ecx", b"edx", b"ebx", b"esp", b"ebp", b"esi", b"edi", b"r8d", b"r9d", b"r10d", b"r11d", b"r12d", b"r13d", b"r14d", b"r15d" },
        "64bit": { b"rax", b"rcx", b"rdx", b"rbx", b"rsp", b"rbp", b"rsi", b"rdi", b"r8", b"r9", b"r10", b"r11", b"r12", b"r13", b"r14", b"r15" },
    }
    # fmt: on

    # invert both mappings for efficient lookup
    widths_inverted: Dict[bytes, RegisterWidth] = {
        name: width for width, names in widths.items() for name in names
    }

    kinds_inverted: Dict[bytes, RegisterKind] = {
        name: kind for kind, names in kinds.items() for name in names
    }

    for rid, entry in registers.items():
        resolution = RegisterResolution(
            accepted=[],
            rejected=[],
        )

        if entry.name not in widths_inverted or entry.name not in kinds_inverted:
            resolution.rejected.append(
                RegisterRejection(
                    ref=entry.ref,
                    reason="unknown-register",
                )
            )

        else:
            resolution.accepted.append(
                RegisterAcceptance(
                    ref=entry.ref,
                    id=rid,
                    name=entry.name,
                    kind=kinds_inverted[entry.name],
                    width=widths_inverted[entry.name],
                )
            )

        resolutions[rid] = resolution

    return OneToOne[RegisterId, RegisterResolution].instance(resolutions)


def check_register_resolution_accepted(
    rule_e3017: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3017) == 0


def build_register_resolution_accepted(
    resolutions: OneToOne[RegisterId, RegisterResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[RegisterId, RegisterAcceptance]:
    accepted: Dict[RegisterId, RegisterAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[RegisterId, RegisterAcceptance].instance(accepted)


def validate_register_resolution_e3017(
    registers: OneToOne[RegisterId, Register],
    resolutions: OneToOne[RegisterId, RegisterResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_register_resolution_e3017(registers.get(id), rejection)
                )

    return diagnostics


def report_register_resolution_e3017(
    entry: Register,
    rejection: RegisterRejection,
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3017",
        message=f"Invalid register {entry}, reason: {rejection.reason}.",
    )
