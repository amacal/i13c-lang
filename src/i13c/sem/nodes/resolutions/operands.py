from typing import Dict, List, Tuple

from i13c.sem.infra import Configuration, OneToOne
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.instructions import Instruction, InstructionId
from i13c.sem.typing.entities.literals import Hex, Literal, LiteralId
from i13c.sem.typing.entities.operands import Immediate, Operand, OperandId, Reference
from i13c.sem.typing.entities.snippets import Slot, Snippet, SnippetId
from i13c.sem.typing.resolutions.callsites import (
    CallSiteAcceptance,
    CallSiteBinding,
    CallSiteResolution,
)
from i13c.sem.typing.resolutions.operands import OperandAcceptance, OperandResolution


def configure_resolution_by_operand() -> Configuration:
    return Configuration(
        builder=build_resolution_by_operand,
        produces=("resolutions/operands",),
        requires=frozenset(
            {
                ("snippets", "entities/snippets"),
                ("instructions", "entities/instructions"),
                ("operands", "entities/operands"),
                ("literals", "entities/literals"),
                ("resolution_by_callsite", "resolutions/callsites"),
            }
        ),
    )


def build_resolution_by_operand(
    snippets: OneToOne[SnippetId, Snippet],
    instructions: OneToOne[InstructionId, Instruction],
    operands: OneToOne[OperandId, Operand],
    literals: OneToOne[LiteralId, Literal],
    resolution_by_callsite: OneToOne[CallSiteId, CallSiteResolution],
) -> OneToOne[OperandId, OperandResolution]:
    resolutions: Dict[OperandId, OperandResolution] = {}
    resolvables: List[Tuple[CallSiteId, CallSiteAcceptance]] = []

    # find all snippet callsites
    for cid, resolution in resolution_by_callsite.items():
        for acceptance in resolution.accepted:
            if acceptance.callable.kind == b"snippet":
                resolvables.append((cid, acceptance))

    for cid, acceptance in resolvables:
        queue: List[OperandId] = []

        # we follow only snippet callables here
        assert isinstance(acceptance.callable.target, SnippetId)
        snippet = snippets.get(acceptance.callable.target)

        # collect all operand references
        for iid in snippet.instructions:
            for oid in instructions.get(iid).operands:
                if operands.get(oid).kind == b"reference":
                    queue.append(oid)

        for oid in queue:
            operand: Operand = operands.get(oid)

            # find the resolution for this operand
            assert isinstance(operand.target, Reference)
            resolutions[oid] = resolve_operand_as_reference(
                literals,
                acceptance.bindings,
                operand.target,
            )

    return OneToOne[OperandId, OperandResolution].instance(resolutions)


def resolve_operand_as_reference(
    literals: OneToOne[LiteralId, Literal],
    bindings: List[CallSiteBinding],
    target: Reference,
) -> OperandResolution:

    acceptances: List[OperandAcceptance] = []

    for binding in bindings:
        # we already prefiltered only slot bindings
        assert isinstance(binding.target, Slot)

        # match slot name with reference name
        if target.name != binding.target.name.name:
            continue

        # only literal can be changed to immediate
        if binding.argument.kind != b"literal":
            continue

        # satisfy type constraint
        assert isinstance(binding.argument.target, LiteralId)

        # fetch referenced literal
        literal = literals.get(binding.argument.target)

        # only hex literals
        if literal.kind != b"hex":
            continue

        # satisfy type constraint
        assert isinstance(literal.target, Hex)

        acceptances.append(
            OperandAcceptance(
                kind=b"immediate",
                target=Immediate(
                    value=literal.target.value,
                    width=binding.type.width,
                ),
            ),
        )

    return OperandResolution(
        accepted=acceptances,
        rejected=[],
    )
