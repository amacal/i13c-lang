from typing import Dict, List, Optional

from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToOne
from i13c.semantic.core import Identifier
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.instructions import Instruction, InstructionId
from i13c.semantic.typing.entities.literals import Hex, Literal, LiteralId
from i13c.semantic.typing.entities.operands import Operand, OperandId
from i13c.semantic.typing.entities.snippets import Slot, Snippet, SnippetId
from i13c.semantic.typing.indices.instances import Instance
from i13c.semantic.typing.resolutions.callsites import (
    CallSiteBinding,
    CallSiteResolution,
)
from i13c.semantic.typing.resolutions.instructions import (
    InstructionResolution,
    ReferenceToImmediate,
    ReferenceToRegister,
)
from i13c.syntax.source import Span


def configure_instance_by_callsite() -> GraphNode:
    return GraphNode(
        builder=build_instances,
        constraint=None,
        produces=("indices/instance-by-callsite",),
        requires=frozenset(
            {
                ("snippets", "entities/snippets"),
                ("literals", "entities/literals"),
                ("operands", "entities/operands"),
                ("instructions", "entities/instructions"),
                ("callsites_resolutions", "resolutions/callsites"),
                ("instructions_resolutions", "resolutions/instructions"),
            }
        ),
    )


def build_instances(
    snippets: OneToOne[SnippetId, Snippet],
    literals: OneToOne[LiteralId, Literal],
    operands: OneToOne[OperandId, Operand],
    instructions: OneToOne[InstructionId, Instruction],
    callsites_resolutions: OneToOne[CallSiteId, CallSiteResolution],
    instructions_resolutions: OneToOne[InstructionId, InstructionResolution],
) -> OneToOne[CallSiteId, Instance]:
    instances: Dict[CallSiteId, Instance] = {}

    for cid, resolution in callsites_resolutions.items():

        # don't generate instance for unresolved callsites
        if len(resolution.accepted) != 1:
            continue

        # here actually is exactly one acceptance
        for callsite_acceptance in resolution.accepted:

            # ignore non-snippet callables
            if callsite_acceptance.callable.kind != b"snippet":
                continue

            # retrieve snippet
            assert isinstance(callsite_acceptance.callable.target, SnippetId)
            snippet = snippets.get(callsite_acceptance.callable.target)

            # collect only non-immediate operand bindings
            bindings: List[CallSiteBinding] = []

            # TODO
            for callsite_binding in callsite_acceptance.bindings:
                if callsite_binding.kind == b"slot":
                    assert isinstance(callsite_binding.target, Slot)
                    if not callsite_binding.target.bind.via_immediate():
                        bindings.append(callsite_binding)

            # collect only rewritten operands
            rewritten: Dict[OperandId, Operand] = {}

            for iid in snippet.instructions:
                # get the instruction behind its id
                instruction = instructions.get(iid)

                for instruction_resolution in instructions_resolutions.get(
                    iid
                ).accepted:
                    instruction_bindings = instruction_resolution.bindings

                    # the resolved bindings should match the instruction operands
                    assert len(instruction_bindings) == len(instruction.operands)

                    # iterate over instruction operands
                    for _, instruction_binding in zip(
                        instruction.operands, instruction_bindings
                    ):
                        # only references-to-immediate can be rewritten
                        if not isinstance(
                            instruction_binding,
                            (ReferenceToImmediate, ReferenceToRegister),
                        ):
                            continue

                        # fetch operand behind the resolved binding
                        oid = instruction_binding.target
                        operand = operands.get(oid)

                        # we need operand as reference, original bindings
                        # and all literals to attempt rewriting
                        args = (
                            operand.ref,
                            instruction_binding.identifier,
                            callsite_acceptance.bindings,
                            literals,
                        )

                        # if operand can be rewritten, do so
                        if new_operand := rewrite_operand(*args):
                            rewritten[oid] = new_operand

            instances[cid] = Instance(
                target=callsite_acceptance.callable.target,
                bindings=bindings,
                operands=rewritten,
            )

    return OneToOne[CallSiteId, Instance].instance(instances)


def rewrite_operand(
    span: Span,
    reference: Identifier,
    bindings: List[CallSiteBinding],
    literals: OneToOne[LiteralId, Literal],
) -> Optional[Operand]:

    # first attempt to find a suitable binding is goo enough
    # because we have guaranteed unique binding names per callsite

    for binding in bindings:

        # satisfy type constraints
        assert isinstance(binding.target, Slot)

        # reference name must match bound slot name
        # we need to find binding for this reference
        if binding.target.name.name != reference.name:
            continue

        # register bindings can rewrite to register operands
        if binding.target.bind.via_register():
            return Operand.register(span, binding.target.bind.name)

        # only immediate bindings can continue
        assert binding.target.bind.via_immediate()

        # only literal arguments can rewrite operands
        if binding.argument.kind != b"literal":
            continue

        # satisfy type constraints
        assert isinstance(binding.argument.target, LiteralId)

        # the literal can be used to rewrite the operand
        literal = literals.get(binding.argument.target)

        # only hex literals can be used
        if literal.kind != b"hex":
            continue

        # satisfy type constraints
        assert isinstance(literal.target, Hex)

        # construct immediate operand from literal value
        return Operand.immediate(span, literal.target.data)

    # failed
    return None
