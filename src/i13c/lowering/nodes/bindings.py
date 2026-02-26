from typing import Dict, List

from i13c.core.dag import GraphNode
from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.typing.blocks import BlockInstruction
from i13c.lowering.typing.flows import BindingFlow, BlockId, FlowId
from i13c.lowering.typing.instructions import (
    InstructionEntry,
    InstructionId,
    MovRegImm,
    MovRegOff,
    Nop,
)
from i13c.lowering.typing.registers import (
    IR_REGISTER_FORWARD,
    VirtualRegister,
    name_to_reg,
)
from i13c.lowering.typing.stacks import StackFrame
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.literals import Hex, LiteralId
from i13c.semantic.typing.entities.parameters import Parameter
from i13c.semantic.typing.entities.snippets import Slot
from i13c.semantic.typing.indices.variables import VariableId
from i13c.semantic.typing.resolutions.callsites import CallSiteBinding


def lower_snippet_bindings(
    graph: SemanticGraph,
    generator: Generator,
    node: CallSiteId,
    bindings: List[CallSiteBinding],
    registers: Dict[VariableId, VirtualRegister],
) -> List[BlockInstruction]:
    out: List[BlockInstruction] = []

    for binding in bindings:
        # because this is a snippet callsite
        assert isinstance(binding.target, Slot)

        # we know slots may be literals
        if binding.argument.kind == b"literal":
            assert isinstance(binding.argument.target, LiteralId)

            literal = graph.basic.literals.get(binding.argument.target)

            # we know all literals are hex for now
            assert literal.kind == b"hex"
            assert isinstance(literal.target, Hex)

            # extract slot binding
            bind = binding.target.bind
            imm = literal.target.value

            # emit move instruction for binding
            iid = InstructionId(value=generator.next())
            instr = MovRegImm(dst=IR_REGISTER_FORWARD[bind.name], imm=imm)

            out.append((iid, instr))

        # or slots may be expressions
        if binding.argument.kind == b"expression":
            assert isinstance(binding.argument.target, ExpressionId)

            expression = graph.basic.expressions.get(binding.argument.target)
            environment = graph.indices.environment_by_flownode.get(node)
            variable = environment.variables[expression.ident]

            src = registers[variable].ref()
            dst = IR_REGISTER_FORWARD[binding.target.bind.name]

            iid = FlowId(value=generator.next())
            instr = BindingFlow(dst=dst, src=src)

            # emit instruction for virtual move
            out.append((iid, instr))

    return out


def lower_function_bindings(
    graph: SemanticGraph,
    generator: Generator,
    node: CallSiteId,
    bindings: List[CallSiteBinding],
    registers: Dict[VariableId, VirtualRegister],
) -> List[BlockInstruction]:
    out: List[BlockInstruction] = []

    for idx, binding in enumerate(bindings):
        # because this is a function callsite
        assert isinstance(binding.target, Parameter)

        # we know parameters may be literals
        if binding.argument.kind == b"literal":
            # satisfy type checker
            assert isinstance(binding.argument.target, LiteralId)

            # find the literal behind the target
            literal = graph.basic.literals.get(binding.argument.target)

            # we know all literals are hex for now
            assert literal.kind == b"hex"
            assert isinstance(literal.target, Hex)

            # extract literal
            imm = literal.target.value

            # emit move instruction for binding
            iid = InstructionId(value=generator.next())
            instr = MovRegImm(dst=idx, imm=imm)

            out.append((iid, instr))

        # or parameters may be expressions
        if binding.argument.kind == b"expression":
            # satisfy type checker
            assert isinstance(binding.argument.target, ExpressionId)

            expression = graph.basic.expressions.get(binding.argument.target)
            environment = graph.indices.environment_by_flownode.get(node)
            variable = environment.variables[expression.ident]

            iid = FlowId(value=generator.next())
            instr = BindingFlow(dst=idx, src=registers[variable].ref())

            # emit instruction for virtual move
            out.append((iid, instr))

    return out


def configure_binding_patching() -> GraphNode:
    return GraphNode(
        builder=patch_bindings,
        constraint=None,
        produces=("llvm/patches/bindings",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("blocks", "llvm/functions/blocks"),
                ("instructions", "llvm/instructions"),
                ("stackframes", "llvm/functions/stackframes"),
            }
        ),
    )


def patch_bindings(
    generator: Generator,
    blocks: OneToMany[FunctionId, BlockId],
    stackframes: OneToOne[FunctionId, StackFrame],
    instructions: OneToMany[BlockId, BlockInstruction],
) -> OneToOne[FlowId, InstructionEntry]:
    bindings: Dict[FlowId, InstructionEntry] = {}

    for fid, bids in blocks.items():
        for bid in bids:
            for iid, instr in instructions.get(bid):
                if not isinstance(iid, FlowId):
                    continue

                if isinstance(instr, BindingFlow):
                    # BindingFlow is referenced by FlowId
                    assert isinstance(iid, FlowId)

                    # find stackframe and get a slot entry
                    stackframe = stackframes.get(fid)
                    offset = stackframe.slot_at_register(instr.src)

                    if offset is None:
                        bindings[iid] = (InstructionId(value=generator.next()), Nop())

                    else:
                        # append new patched binding
                        bindings[iid] = (
                            InstructionId(value=generator.next()),
                            MovRegOff(
                                dst=instr.dst, src=name_to_reg("rsp"), off=offset * 8
                            ),
                        )

    return OneToOne[FlowId, InstructionEntry].instance(bindings)
