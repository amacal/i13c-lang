from typing import Any, Dict, List, Optional

from i13c.core.diagnostics import Diagnostic
from i13c.core.graph import GraphGroup, GraphNode
from i13c.core.mapping import OneToOne
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
    )

    return GraphGroup(nodes=[resolve, validate, extract])


def build_instruction_resolution(
    instructions: OneToOne[InstructionId, Instruction],
    snippets: OneToOne[SnippetId, Snippet],
    mnemonics: OneToOne[MnemonicId, MnemonicAcceptance],
    operands: OneToOne[OperandId, OperandAcceptance],
) -> OneToOne[InstructionId, InstructionResolution]:
    resolutions: Dict[InstructionId, InstructionResolution] = {}

    for iid, entry in instructions.items():
        resolution = InstructionResolution(
            accepted=[],
            rejected=[],
        )

        # fetch already resolved mnemonic
        mnemonic = mnemonics.get(entry.mnemonic)

        # to iterate over all its variants
        for variant in mnemonic.variants:
            collected: List[OperandAcceptance] = []

            if len(variant) != len(entry.operands):
                resolution.rejected.append(
                    InstructionRejection(
                        ref=entry.ref,
                        reason="arity-mismatch",
                    )
                )

                continue

            for spec, op in zip(variant, entry.operands):
                accepted = operands.get(op)
                reason: Optional[InstructionRejectionReason] = None

                if accepted.symbol != spec.symbol:
                    reason = "variant-mismatch"

                if spec.names and not reason:
                    if not isinstance(accepted.target, RegisterAcceptance):
                        reason = "register-mismatch"

                    elif accepted.target.name not in spec.names:
                        reason = "register-mismatch"

                if reason is not None:
                    resolution.rejected.append(
                        InstructionRejection(
                            ref=entry.ref,
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
                    reason="variant-mismatch",
                )
            )

        resolutions[iid] = resolution

    return OneToOne[InstructionId, InstructionResolution].instance(resolutions)


def check_instruction_resolution_accepted(
    rule_e3023: List[Diagnostic],
    **kwargs: Dict[str, Any],
) -> bool:
    return len(rule_e3023) == 0


def build_instruction_resolution_accepted(
    resolutions: OneToOne[InstructionId, InstructionResolution],
    **kwargs: Dict[str, Any],
) -> OneToOne[InstructionId, InstructionAcceptance]:
    accepted: Dict[InstructionId, InstructionAcceptance] = {}

    for id, resolution in resolutions.items():
        accepted[id] = resolution.accepted[0]

    return OneToOne[InstructionId, InstructionAcceptance].instance(accepted)


def validate_instruction_resolution_e3023(
    instructions: OneToOne[InstructionId, Instruction],
    resolutions: OneToOne[InstructionId, InstructionResolution],
) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []

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
        message=f"Invalid instruction {str(entry)}, reason: {rejection.reason}.",
    )
