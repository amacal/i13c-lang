from typing import Dict, List

from i13c.core.generator import Generator
from i13c.core.graph import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.llvm.typing.blocks import BlockInstruction
from i13c.llvm.typing.flows import BindingFlow, BlockId, FlowId
from i13c.llvm.typing.instructions import InstructionEntry, InstructionId
from i13c.llvm.typing.instructions.core import (
    ComputedAddress,
    Displacement,
    Immediate,
    Register,
    Scaler,
)
from i13c.llvm.typing.instructions.ctrl import Nop
from i13c.llvm.typing.instructions.move import MovRegImm, MovRegOff
from i13c.llvm.typing.registers import VirtualRegister, name_to_reg64
from i13c.llvm.typing.stacks import StackFrame
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.bindings import CallSiteBindings
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.literals import Hex, LiteralId
from i13c.semantic.typing.entities.parameters import Parameter
from i13c.semantic.typing.entities.snippets import Slot
from i13c.semantic.typing.indices.variables import VariableId


def lower_snippet_bindings(
    graph: SemanticGraph,
    generator: Generator,
    bindings: CallSiteBindings,
    registers: OneToOne[VariableId, VirtualRegister],
) -> List[BlockInstruction]:
    out: List[BlockInstruction] = []

    for binding in bindings.entries:

        assert isinstance(binding.dst, Slot)

        # we know slots may be literals
        if isinstance(binding.src, LiteralId):

            # find the literal behind the target
            literal = graph.entities.literals.get(binding.src)

            # we know all literals are hex for now
            assert literal.kind == b"hex"
            assert isinstance(literal.target, Hex)

            # extract slot binding
            bind = binding.dst.bind
            imm = Immediate(data=literal.target.data, width=literal.target.width)

            # emit move instruction for binding
            iid = InstructionId(value=generator.next())
            instr = MovRegImm(dst=name_to_reg64(bind.name.decode()), imm=imm)

            out.append((iid, instr))

        # or slots may be expressions
        if isinstance(binding.src, VariableId):
            src = registers.get(binding.src).ref()
            dst = name_to_reg64(binding.dst.bind.name.decode())

            iid = FlowId(value=generator.next())
            instr = BindingFlow(dst=dst, src=src)

            # emit instruction for virtual move
            out.append((iid, instr))

    return out


def lower_function_bindings(
    graph: SemanticGraph,
    generator: Generator,
    bindings: CallSiteBindings,
    registers: OneToOne[VariableId, VirtualRegister],
) -> List[BlockInstruction]:
    out: List[BlockInstruction] = []

    for idx, binding in enumerate(bindings.entries):

        assert isinstance(binding.dst, Parameter)

        # we know parameters may be literals
        if isinstance(binding.src, LiteralId):

            # find the literal behind the target
            literal = graph.entities.literals.get(binding.src)

            # we know all literals are hex for now
            assert literal.kind == b"hex"
            assert isinstance(literal.target, Hex)

            # extract literal
            imm = Immediate(data=literal.target.data, width=literal.target.width)

            # emit move instruction for binding
            iid = InstructionId(value=generator.next())
            instr = MovRegImm(dst=idx, imm=imm)

            out.append((iid, instr))

        # or parameters may be expressions
        if isinstance(binding.src, VariableId):

            # emit move instruction for binding
            iid = FlowId(value=generator.next())
            instr = BindingFlow(dst=idx, src=registers.get(binding.src).ref())

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
) -> OneToMany[FlowId, InstructionEntry]:
    bindings: Dict[FlowId, List[InstructionEntry]] = {}

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
                        bindings[iid] = [(InstructionId(value=generator.next()), Nop())]

                    else:
                        disp32 = (offset * 8).to_bytes(4, byteorder="big", signed=False)

                        # append new patched binding
                        bindings[iid] = [
                            (
                                InstructionId(value=generator.next()),
                                MovRegOff(
                                    dst=instr.dst,
                                    src=ComputedAddress(
                                        base=Register.parse64("rsp"),
                                        disp=Displacement.auto(disp32),
                                        scaler=Scaler.none(),
                                        width=64,
                                    ),
                                ),
                            )
                        ]

    return OneToMany[FlowId, InstructionEntry].instance(bindings)
