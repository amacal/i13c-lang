from collections.abc import Iterable
from typing import Any

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode, GraphViews
from i13c.core.mapping import OneToMany, OneToOne
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.entities.mnemonics import MnemonicId
from i13c.semantic.typing.entities.operands import OperandId
from i13c.semantic.typing.entities.snippets import Snippet, SnippetId
from i13c.semantic.typing.resolutions.instructions import (
    InstructionAcceptance,
    InstructionRejection,
    InstructionRejectionReason,
    InstructionResolution,
)
from i13c.semantic.typing.resolutions.mnemonics import MnemonicAcceptance
from i13c.semantic.typing.resolutions.operands import OperandAcceptance
from i13c.semantic.typing.resolutions.registers import RegisterAcceptance


def configure_instruction_resolution() -> GraphGroup:
    resolve = GraphNode(
        builder=build_instruction_resolution,
        constraint=None,
        produces=("resolutions/instructions",),
        requires=frozenset(
            {
                ("instructions", "entities/instructions"),
                ("snippets", "entities/snippets"),
                ("mnemonics", "resolutions/mnemonics/accepted"),
                ("operands", "resolutions/operands/accepted"),
            }
        ),
        views=GraphViews(list=ListAllExtractor),
    )

    validate = GraphNode(
        builder=validate_instruction_resolution_e3023,
        constraint=None,
        produces=("rules/e3023",),
        requires=frozenset(
            {
                ("instructions", "entities/instructions"),
                ("resolutions", "resolutions/instructions"),
            }
        ),
    )

    extract = GraphNode(
        builder=build_instruction_resolution_accepted,
        constraint=check_instruction_resolution_accepted,
        produces=("resolutions/instructions/accepted",),
        requires=frozenset(
            {
                ("rule_e3023", "rules/e3023"),
                ("resolutions", "resolutions/instructions"),
            }
        ),
        views=GraphViews(list=ListAcceptedExtractor),
    )

    reject = GraphNode(
        builder=build_instruction_resolution_rejected,
        constraint=None,
        produces=("resolutions/instructions/rejected",),
        requires=frozenset({("resolutions", "resolutions/instructions")}),
        views=GraphViews(list=ListRejectedExtractor),
    )

    return GraphGroup(nodes=[resolve, validate, extract, reject])


def build_instruction_resolution(
    instructions: OneToOne[InstructionId, Instruction],
    snippets: OneToOne[SnippetId, Snippet],
    mnemonics: OneToOne[MnemonicId, MnemonicAcceptance],
    operands: OneToOne[OperandId, OperandAcceptance],
) -> OneToOne[InstructionId, InstructionResolution]:
    resolutions: dict[InstructionId, InstructionResolution] = {}

    for iid, entry in instructions.items():
        resolution = InstructionResolution(
            ref=entry.ref,
            id=iid,
            accepted=[],
            rejected=[],
        )

        # fetch already resolved mnemonic
        mnemonic = mnemonics.get(entry.mnemonic)

        # to iterate over all its variants
        for variant in mnemonic.variants:
            collected: list[OperandAcceptance] = []

            if len(variant) != len(entry.operands):
                resolution.rejected.append(
                    InstructionRejection(
                        ref=entry.ref,
                        id=iid,
                        target=entry,
                        mnemonic=mnemonic,
                        variant=variant,
                        operands=None,
                        reason="arity-mismatch",
                    )
                )

                continue

            for spec, op in zip(variant, entry.operands):
                accepted = operands.get(op)
                reason: InstructionRejectionReason | None = None

                if accepted.symbol != spec.symbol:
                    reason = "variant-mismatch"

                if spec.names and not reason: # noqa: SIM102
                    if not isinstance(accepted.target, RegisterAcceptance) or accepted.target.name not in spec.names:
                        reason = "register-mismatch"

                if reason is not None:
                    resolution.rejected.append(
                        InstructionRejection(
                            ref=entry.ref,
                            id=iid,
                            target=entry,
                            mnemonic=mnemonic,
                            variant=variant,
                            operands=tuple(collected),
                            reason=reason,
                        )
                    )

                else:
                    collected.append(accepted)

            if len(variant) == len(collected):

                index, idx = -1, -1
                snippet_id = entry.get_snippet(SnippetId.from_context)

                for id in snippets.get(snippet_id).body:
                    if isinstance(id, InstructionId):
                        idx += 1

                        if iid == id:
                            index = idx
                            break

                assert index >= 0

                resolution.accepted.append(
                    InstructionAcceptance(
                        ref=entry.ref,
                        id=iid,
                        index=index,
                        mnemonic=mnemonic,
                        operands=tuple(collected),
                        variant=variant,
                    )
                )

        if not resolution.accepted:
            resolution.rejected.append(
                InstructionRejection(
                    ref=entry.ref,
                    id=iid,
                    target=entry,
                    mnemonic=mnemonic,
                    variant=None,
                    operands=None,
                    reason="variant-mismatch",
                )
            )

        resolutions[iid] = resolution

    return OneToOne[InstructionId, InstructionResolution].instance(resolutions)


def check_instruction_resolution_accepted(
    rule_e3023: list[Diagnostic],
    **kwargs: dict[str, Any],
) -> bool:
    return len(rule_e3023) == 0


def build_instruction_resolution_accepted(
    resolutions: OneToOne[InstructionId, InstructionResolution],
    **kwargs: dict[str, Any],
) -> OneToOne[InstructionId, InstructionAcceptance]:
    accepted: dict[InstructionId, InstructionAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[InstructionId, InstructionAcceptance].instance(accepted)


def build_instruction_resolution_rejected(
    resolutions: OneToOne[InstructionId, InstructionResolution],
    **kwargs: dict[str, Any],
) -> OneToMany[InstructionId, InstructionRejection]:
    rejected: dict[InstructionId, list[InstructionRejection]] = {}

    for id, resolution in resolutions.items():
        rejected[id] = resolution.rejected

    return OneToMany[InstructionId, InstructionRejection].instance(rejected)


def validate_instruction_resolution_e3023(
    instructions: OneToOne[InstructionId, Instruction],
    resolutions: OneToOne[InstructionId, InstructionResolution],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for id, resolution in resolutions.items():
        if len(resolution.accepted) != 1:
            for rejection in resolution.rejected:
                diagnostics.append(
                    report_instruction_resolution_e3023(instructions.get(id), rejection)
                )

    return diagnostics


def report_instruction_resolution_e3023(
    entry: Instruction, rejection: InstructionRejection
) -> Diagnostic:
    return Diagnostic(
        ref=rejection.ref,
        code="E3023",
        message=f"Invalid instruction {entry!s}, reason: {rejection.reason}.",
    )



class ListAllExtractor:
    def __init__(self, data: OneToOne[InstructionId, InstructionResolution]):
        self.data = data

    def extract(self) -> Iterable[tuple[InstructionId, InstructionResolution]]:
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
    def rows(key: InstructionId, entry: InstructionResolution) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "accepted": str(len(entry.accepted)),
            "rejected": str(len(entry.rejected)),
        }


class ListRejectedExtractor:
    def __init__(self, data: OneToMany[InstructionId, InstructionRejection]):
        self.data = data

    def extract(self) -> Iterable[tuple[InstructionId, InstructionRejection]]:
        for key, entries in self.data.items():
            for entry in entries:
                yield key, entry

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "mnemonic": "Mnemonic",
            "variant": "Variant",
            "operands": "Operands",
            "reason": "Reason",
        }

    @staticmethod
    def rows(key: InstructionId, entry: InstructionRejection) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "mnemonic": entry.mnemonic.name.decode(),
            "variant": ", ".join(spec.symbol for spec in entry.variant) if entry.variant else "",
            "operands": ", ".join(str(op.target) for op in entry.operands) if entry.operands else "",
            "reason": entry.reason,
        }


class ListAcceptedExtractor:
    def __init__(self, data: OneToOne[InstructionId, InstructionAcceptance]):
        self.data = data

    def extract(self) -> Iterable[tuple[InstructionId, InstructionAcceptance]]:
        yield from self.data.items()

    @staticmethod
    def headers() -> dict[str, str]:
        return {
            "ref": "Ref",
            "id": "ID",
            "idx": "Index",
            "mnemonic": "Mnemonic",
            "variant": "Variant",
            "operands": "Operands",
        }

    @staticmethod
    def rows(key: InstructionId, entry: InstructionAcceptance) -> dict[str, str]:
        return {
            "ref": str(entry.ref),
            "id": key.identify(1),
            "idx": str(entry.index),
            "mnemonic": entry.mnemonic.name.decode(),
            "variant": ", ".join(spec.symbol for spec in entry.variant),
            "operands": ", ".join(str(op.target) for op in entry.operands),
        }
