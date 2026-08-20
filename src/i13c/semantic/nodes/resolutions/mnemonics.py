from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.mnemonics import Mnemonic, MnemonicId
from i13c.semantic.typing.resolutions.mnemonics import (
    MnemonicAcceptance,
    MnemonicOperandSpec,
    MnemonicRejection,
    MnemonicResolution,
    MnemonicVariant,
)

INSTRUCTIONS_TABLE: dict[bytes, list[MnemonicVariant]] = {
    b"add": [
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.reg64()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm32()),
    ],
    b"and": [
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.reg64()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.reg32()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg16(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg16(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg16(), MnemonicOperandSpec.reg16()),
        (MnemonicOperandSpec.reg8(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg8(), MnemonicOperandSpec.reg8()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.reg64()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.reg32()),
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
    b"loop": [
        (MnemonicOperandSpec.rel(),),
    ],
    b"mov": [
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm64()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.reg64()),
        (MnemonicOperandSpec.reg8(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg16(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.reg8()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.reg16()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.reg32()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.reg64()),
    ],
    b"nop": [()],
    b"or": [
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.reg64()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.reg32()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.addr()),
        (MnemonicOperandSpec.reg16(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg16(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.reg16(), MnemonicOperandSpec.reg16()),
        (MnemonicOperandSpec.reg8(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg8(), MnemonicOperandSpec.reg8()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm16()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.imm32()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.reg64()),
        (MnemonicOperandSpec.addr(), MnemonicOperandSpec.reg32()),
    ],
    b"ret": [()],
    b"shl": [
        (MnemonicOperandSpec.reg8(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg16(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg32(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.imm8()),
        (MnemonicOperandSpec.reg64(), MnemonicOperandSpec.reg8(b"cl")),
    ],
    b"shr": [
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
        views=GraphViews(list=ListAllExtractor),
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
        views=GraphViews(list=ListAcceptedExtractor),
    )

    reject = GraphNode(
        builder=build_mnemonic_resolution_rejected,
        constraint=None,
        produces=("resolutions/mnemonics/rejected",),
        requires=frozenset({("resolutions", "resolutions/mnemonics")}),
        views=GraphViews(list=ListRejectedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract, reject])


def build_mnemonic_resolution(
    mnemonics: OneToOne[MnemonicId, Mnemonic],
) -> OneToOne[MnemonicId, MnemonicResolution]:
    resolutions: dict[MnemonicId, MnemonicResolution] = {}

    for mid, entry in mnemonics.items():
        resolution = MnemonicResolution(
            ref=entry.ref,
            id=mid,
            accepted=[],
            rejected=[],
        )

        if entry.name not in INSTRUCTIONS_TABLE:
            resolution.rejected.append(
                MnemonicRejection(
                    ref=entry.ref,
                    id=mid,
                    target=entry,
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
    rule_e3024: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3024) == 0


def build_mnemonic_resolution_accepted(
    resolutions: OneToOne[MnemonicId, MnemonicResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[MnemonicId, MnemonicAcceptance]:
    accepted: dict[MnemonicId, MnemonicAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[MnemonicId, MnemonicAcceptance].instance(accepted)


def build_mnemonic_resolution_rejected(
    resolutions: OneToOne[MnemonicId, MnemonicResolution],
    **kwargs: dict[str, Any],
) -> OneToMany[MnemonicId, MnemonicRejection]:
    rejected: dict[MnemonicId, list[MnemonicRejection]] = {}

    for id, resolution in resolutions.items():
        rejected[id] = resolution.rejected

    return OneToMany[MnemonicId, MnemonicRejection].instance(rejected)


def validate_mnemonic_resolution_e3024(
    mnemonics: OneToOne[MnemonicId, Mnemonic],
    resolutions: OneToOne[MnemonicId, MnemonicResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

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


class ListAllExtractor:
    def __init__(self, data: OneToOne[MnemonicId, MnemonicResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[MnemonicId, MnemonicResolution]]:
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
    def rows(key: MnemonicId, entry: MnemonicResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListRejectedExtractor:
    def __init__(self, data: OneToMany[MnemonicId, MnemonicRejection]):
        self.data = data

    def extract(self) -> Iterable[tuple[MnemonicId, MnemonicRejection]]:
        for key, entries in self.data.items():
            for entry in entries:
                yield key, entry

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "reason": "Reason",
        }

    @staticmethod
    def rows(key: MnemonicId, entry: MnemonicRejection) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.target.name.decode(),
            "reason": entry.reason,
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[MnemonicId, MnemonicAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[MnemonicId, MnemonicAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "name": "Name",
            "variants": "Variants",
        }

    @staticmethod
    def rows(key: MnemonicId, entry: MnemonicAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "name": entry.name.decode(),
            "variants": str(len(entry.variants)),
        }
