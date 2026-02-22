from typing import Dict, List

from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.typing.blocks import BlockInstruction
from i13c.lowering.typing.flows import BindingFlow, BlockId, FlowId
from i13c.lowering.typing.instructions import (
    InstructionEntry,
    InstructionId,
    MovRegImm,
    MovRegReg,
)
from i13c.lowering.typing.registers import IR_REGISTER_FORWARD
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import Hex, LiteralId
from i13c.semantic.typing.entities.parameters import Parameter
from i13c.semantic.typing.entities.snippets import Slot
from i13c.semantic.typing.resolutions.callsites import CallSiteBinding


def lower_snippet_bindings(
    graph: SemanticGraph, bindings: List[CallSiteBinding]
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
            iid = InstructionId(value=graph.generator.next())
            instr = MovRegImm(dst=IR_REGISTER_FORWARD[bind.name], imm=imm)

            out.append((iid, instr))

        # or slots may be expressions
        if binding.argument.kind == b"expression":
            assert isinstance(binding.argument.target, ExpressionId)

            src = binding.argument.target
            dst = IR_REGISTER_FORWARD[binding.target.bind.name]

            # emit flow binding to be patched later
            fid = FlowId(value=graph.generator.next())
            flow = BindingFlow(dst=dst, src=src)

            out.append((fid, flow))

    return out


def lower_function_bindings(
    graph: SemanticGraph, bindings: List[CallSiteBinding]
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
            iid = InstructionId(value=graph.generator.next())
            instr = MovRegImm(dst=idx, imm=imm)

            out.append((iid, instr))

        # or parameters may be expressions
        if binding.argument.kind == b"expression":
            # satisfy type checker
            assert isinstance(binding.argument.target, ExpressionId)

            src = binding.argument.target
            dst = idx

            fid = FlowId(value=graph.generator.next())
            flow = BindingFlow(dst=dst, src=src)

            # emit flow binding to be patched later
            out.append((fid, flow))

    return out


def configure_binding_patching() -> GraphNode:
    return GraphNode(
        builder=patch_bindings,
        constraint=None,
        produces=("llvm/patches/bindings",),
        requires=frozenset(
            {
                ("graph", "semantic/graph"),
                ("instructions", "llvm/blocks/instructions"),
            }
        ),
    )


def patch_bindings(
    graph: SemanticGraph, instructions: OneToMany[BlockId, BlockInstruction]
) -> OneToOne[FlowId, InstructionEntry]:
    mapping: Dict[ExpressionId, int] = {}
    bindings: Dict[FlowId, InstructionEntry] = {}

    for cid, callsite in graph.basic.callsites.items():
        environment = graph.indices.environment_by_flownode.get(cid)

        for arg in callsite.arguments:
            if arg.kind != b"expression":
                continue

            # satisfy type checker
            assert isinstance(arg.target, ExpressionId)

            expression = graph.basic.expressions.get(arg.target)
            vid = environment.variables[expression.ident]

            variable = graph.basic.variables.get(vid)
            function = graph.basic.functions.get(environment.owner)

            for idx, pid in enumerate(function.parameters):
                if pid == variable.source:
                    mapping[arg.target] = idx

    for batch in instructions.values():
        for fid, flow in batch:
            if isinstance(flow, BindingFlow):
                # BindingFlow is referenced by FlowId
                assert isinstance(fid, FlowId)

                # append new patched binding
                bindings[fid] = (
                    InstructionId(value=graph.generator.next()),
                    MovRegReg(dst=flow.dst, src=mapping[flow.src]),
                )

    return OneToOne[FlowId, InstructionEntry].instance(bindings)
