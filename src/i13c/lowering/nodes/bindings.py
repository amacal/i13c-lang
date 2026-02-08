from typing import Dict, List

from i13c.lowering.graph import LowLevelContext
from i13c.lowering.nodes.registers import IR_REGISTER_MAP
from i13c.lowering.typing.blocks import BlockInstruction
from i13c.lowering.typing.flows import BindingFlow
from i13c.lowering.typing.instructions import MovRegImm, MovRegReg
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.expressions import ExpressionId
from i13c.semantic.typing.entities.literals import Hex, LiteralId
from i13c.semantic.typing.entities.parameters import Parameter
from i13c.semantic.typing.entities.snippets import Slot
from i13c.semantic.typing.resolutions.callsites import CallSiteBinding


def lower_snippet_bindings(
    ctx: LowLevelContext, bindings: List[CallSiteBinding]
) -> List[BlockInstruction]:
    out: List[BlockInstruction] = []

    for binding in bindings:
        # because this is a snippet callsite
        assert isinstance(binding.target, Slot)

        # we know slots may be literals
        if binding.argument.kind == b"literal":
            assert isinstance(binding.argument.target, LiteralId)

            literal = ctx.graph.basic.literals.get(binding.argument.target)

            # we know all literals are hex for now
            assert literal.kind == b"hex"
            assert isinstance(literal.target, Hex)

            # extract slot binding
            bind = binding.target.bind
            imm = literal.target.value

            # emit move instruction for binding
            out.append(MovRegImm(dst=IR_REGISTER_MAP[bind.name], imm=imm))

        # or slots may be expressions
        if binding.argument.kind == b"expression":
            assert isinstance(binding.argument.target, ExpressionId)

            # emit flow binding to be patched later
            out.append(
                BindingFlow(
                    dst=IR_REGISTER_MAP[binding.target.bind.name],
                    src=binding.argument.target,
                )
            )

    return out


def lower_function_bindings(
    ctx: LowLevelContext, bindings: List[CallSiteBinding]
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
            literal = ctx.graph.basic.literals.get(binding.argument.target)

            # we know all literals are hex for now
            assert literal.kind == b"hex"
            assert isinstance(literal.target, Hex)

            # extract literal
            imm = literal.target.value

            # emit move instruction for binding
            out.append(MovRegImm(dst=idx, imm=imm))

        # or parameters may be expressions
        if binding.argument.kind == b"expression":
            # satisfy type checker
            assert isinstance(binding.argument.target, ExpressionId)

            # emit flow binding to be patched later
            out.append(
                BindingFlow(
                    dst=idx,
                    src=binding.argument.target,
                )
            )

    return out


def patch_bindings(ctx: LowLevelContext) -> None:

    values: Dict[ExpressionId, int] = {}

    for cid, callsite in ctx.graph.basic.callsites.items():
        environment = ctx.graph.indices.environment_by_flownode.get(cid)

        for arg in callsite.arguments:
            if arg.kind != b"expression":
                continue

            # satisfy type checker
            assert isinstance(arg.target, ExpressionId)

            expression = ctx.graph.basic.expressions.get(arg.target)
            vid = environment.variables[expression.ident]

            variable = ctx.graph.basic.variables.get(vid)
            function = ctx.graph.basic.functions.get(environment.owner)

            for idx, pid in enumerate(function.parameters):
                if pid == variable.source:
                    values[arg.target] = idx

    for block in ctx.nodes.values():
        # only callsite blocks may have binding flows
        if not isinstance(block.origin, CallSiteId):
            continue

        # patch all bindings with an actual move
        for idx, instr in enumerate(block.instructions):
            if isinstance(instr, BindingFlow):
                block.instructions[idx] = MovRegReg(
                    dst=instr.dst,
                    src=values[instr.src],
                )
