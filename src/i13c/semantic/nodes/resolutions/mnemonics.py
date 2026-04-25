from typing import Any, Dict, List

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.typing.entities.mnemonics import Mnemonic, MnemonicId
from i13c.semantic.typing.resolutions.mnemonics import (
    MnemonicAcceptance,
    MnemonicOperandSpec,
    MnemonicRejection,
    MnemonicResolution,
    MnemonicVariant,
)

INSTRUCTIONS_TABLE: Dict[bytes, List[MnemonicVariant]] = {
    b"add": [
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.reg64()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm32()),
    ],
    b"bswap": [
        (MnemonicOperandSpec.reg32(),),
        (MnemonicOperandSpec.reg64(),),
    ],
    b"jmp": [
        (MnemonicOperandSpec.addr(),),
        (MnemonicOperandSpec.reg64(),),
        (MnemonicOperandSpec.rel(),),
    ],
    b"lea": [
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.addr()),
    ],
    b"mov": [
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm64()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.reg64()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.reg64()),
    ],
    b"nop": [()],
    b"shl": [
        (MnemonicOperandSpec.reg8(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg16(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.reg8(b"cl")),
    ],
    b"syscall": [()],
}


def configure_mnemonic_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_mnemonic_resolution,
        constraint=None,
        produces=("resolutions/mnemonics",),
        requires=frozenset({("mnemonics", "entities/mnemonics")}),
    )

    validate = GraphNode(
        builder=validate_mnemonic_resolution_e3024,
        constraint=None,
        produces=("rules/e3024",),
        requires=frozenset(
            {
                ("mnemonics", "entities/mnemonics"),
                ("resolutions", "resolutions/mnemonics"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_mnemonic_resolution_accepted,
        constraint=check_mnemonic_resolution_accepted,
        produces=("resolutions/mnemonics/accepted",),
        requires=frozenset(
            {
                ("rule_e3024", "rules/e3024"),
                ("resolutions", "resolutions/mnemonics"),
            }
        ),
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_mnemonic_resolution(
    mnemonics: OneToOne[MnemonicId, Mnemonic],
) -> OneToOne[MnemonicId, MnemonicResolution]:
    resolutions: Dict[MnemonicId, MnemonicResolution] = {}

    for mid, entry in mnemonics.items():
        resolution = MnemonicResolution(
            accepted=[],
            rejected=[],
        )

        if entry.name not in INSTRUCTIONS_TABLE:
            resolution.rejected.append(
                MnemonicRejection(
                    ref=entry.ref,
                    reason="unknown-mnemonic",
                )
            )

        else:
            resolution.accepted.append(
                MnemonicAcceptance(
                    ref=entry.ref,
                    id=mid,
                    name=entry.name,
                    variants=INSTRUCTIONS_TABLE[entry.name],
                )
            )

        resolutions[mid] = resolution

    return OneToOne[MnemonicId, MnemonicResolution].instance(resolutions)


def check_mnemonic_resolution_accepted(
    rule_e3024: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3024) == 0


def build_mnemonic_resolution_accepted(
    resolutions: OneToOne[MnemonicId, MnemonicResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[MnemonicId, MnemonicAcceptance]:
    accepted: Dict[MnemonicId, MnemonicAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[MnemonicId, MnemonicAcceptance].instance(accepted)


def validate_mnemonic_resolution_e3024(
    mnemonics: OneToOne[MnemonicId, Mnemonic],
    resolutions: OneToOne[MnemonicId, MnemonicResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_mnemonic_resolution_e3024(mnemonics.get(id), rejection)
                )

    return diagnostics


def report_mnemonic_resolution_e3024(
    entry: Mnemonic, rejection: MnemonicRejection
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3024",
        message=f"Invalid mnemonic {entry.name.decode()}, reason: {rejection.reason}.",
    )
