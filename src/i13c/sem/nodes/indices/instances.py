from typing import Dict, List, Optional

from i13c.core.mapping import OneToOne
from i13c.sem.infra import Configuration
from i13c.sem.typing.entities.callsites import CallSiteId
from i13c.sem.typing.entities.instructions import Instruction, InstructionId
from i13c.sem.typing.entities.literals import Hex, Literal, LiteralId
from i13c.sem.typing.entities.operands import Operand, OperandId, Reference
from i13c.sem.typing.entities.snippets import Slot, Snippet, SnippetId
from i13c.sem.typing.indices.instances import Instance
from i13c.sem.typing.resolutions.callsites import CallSiteBinding, CallSiteResolution


def configure_instance_by_callsite() -> Configuration:
    return Configuration(
        builder=build_instances,
        produces=("indices/instance-by-callsite",),
        requires=frozenset(
            {
                ("snippets", "entities/snippets"),
                ("literals", "entities/literals"),
                ("operands", "entities/operands"),
                ("instructions", "entities/instructions"),
                ("resolutions", "resolutions/callsites"),
            }
        ),
    )


def build_instances(
    snippets: OneToOne[SnippetId, Snippet],
    literals: OneToOne[LiteralId, Literal],
    operands: OneToOne[OperandId, Operand],
    instructions: OneToOne[InstructionId, Instruction],
    resolutions: OneToOne[CallSiteId, CallSiteResolution],
) -> OneToOne[CallSiteId, Instance]:
    instances: Dict[CallSiteId, Instance] = {}

    for cid, resolution in resolutions.items():

        # don't generate instance for unresolved callsites
        if len(resolution.accepted) != 1:
            continue

        # here actually is exactly one acceptance
        for acceptance in resolution.accepted:

            # ignore non-snippet callables
            if acceptance.callable.kind != b"snippet":
                continue

            # retrieve snippet
            assert isinstance(acceptance.callable.target, SnippetId)
            snippet = snippets.get(acceptance.callable.target)

            # collect only non-immediate operand bindings
            bindings: List[CallSiteBinding] = []

            for binding in acceptance.bindings:
                if binding.kind == b"slot":
                    assert isinstance(binding.target, Slot)
                    if not binding.target.bind.via_immediate():
                        bindings.append(binding)

            # collect only rewritten operands
            rewritten: Dict[OperandId, Operand] = {}

            for iid in snippet.instructions:
                instruction = instructions.get(iid)

                # iterate over instruction operands
                for oid in instruction.operands:
                    operand = operands.get(oid)

                    # only references can be rewritten
                    if operand.kind != b"reference":
                        continue

                    # satisfy type constraints
                    assert isinstance(operand.target, Reference)

                    # we need operand as reference, original bindings
                    # and all literals to attempt rewriting
                    args = (operand.target, acceptance.bindings, literals)

                    # if operand can be rewritten, do so
                    if new_operand := rewrite_operand(*args):
                        rewritten[oid] = new_operand

            instances[cid] = Instance(
                target=acceptance.callable.target,
                bindings=bindings,
                operands=rewritten,
            )

    return OneToOne[CallSiteId, Instance].instance(instances)


def rewrite_operand(
    reference: Reference,
    bindings: List[CallSiteBinding],
    literals: OneToOne[LiteralId, Literal],
) -> Optional[Operand]:

    # first attempt to find a suitable binding is goo enough
    # because we have guaranteed unique binding names per callsite

    for binding in bindings:

        # only slot bindings can rewrite operands
        if binding.kind != b"slot":
            continue

        # only literal arguments can rewrite operands
        if binding.argument.kind != b"literal":
            continue

        # satisfy type constraints
        assert isinstance(binding.target, Slot)
        assert isinstance(binding.argument.target, LiteralId)

        # reference name must match bound slot name
        if binding.target.name.name != reference.name:
            continue

        # the literal can be used to rewrite the operand
        literal = literals.get(binding.argument.target)

        # only hex literals can be used
        if literal.kind != b"hex":
            continue

        # satisfy type constraints
        assert isinstance(literal.target, Hex)

        # construct immediate operand from literal value
        return Operand.immediate(value=literal.target.value)

    # failed
    return None
