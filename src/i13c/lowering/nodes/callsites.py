from typing import Dict, List

from i13c.core.dag import GraphNode
from i13c.core.generator import Generator
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.nodes.bindings import lower_function_bindings, lower_snippet_bindings
from i13c.lowering.nodes.instances import lower_instance
from i13c.lowering.typing.blocks import BlockInstruction
from i13c.lowering.typing.flows import (
    BlockId,
    CallFlow,
    ClobbersFlow,
    FlowId,
)
from i13c.lowering.typing.instructions import Call, InstructionEntry, InstructionId, Nop
from i13c.lowering.typing.registers import VirtualRegister, name_to_reg
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.indices.variables import VariableId


def lower_callsite(
    generator: Generator,
    graph: SemanticGraph,
    node: CallSiteId,
    registers: OneToOne[VariableId, VirtualRegister],
) -> List[BlockInstruction]:

    # prepare instructions
    instructions: List[BlockInstruction] = []

    # retrieve callsite bindings
    bindings = graph.basic.bindings.get(node)

    if isinstance(bindings.callable.target, SnippetId):
        instance = graph.indices.instance_by_callsite.get(node)
        target = bindings.callable.target

        snippet = graph.basic.snippets.get(target)
        clobbers = [name_to_reg(reg.name.decode()) for reg in snippet.clobbers]

        # append callsite specific bindings
        instructions.extend(
            lower_snippet_bindings(graph, generator, bindings, registers)
        )

        # append emitted instructions
        instructions.extend(lower_instance(graph, generator, instance))

        if clobbers:
            # append callsite snippet flow
            iid = FlowId(value=generator.next())
            instructions.extend([(iid, ClobbersFlow(clobbers=clobbers))])

    else:

        # extract successfully resolved target
        target = bindings.callable.target

        # append callsite specific bindings
        instructions.extend(
            lower_function_bindings(graph, generator, bindings, registers)
        )

        # append callsite call instructions
        iid = FlowId(value=generator.next())
        instructions.extend([(iid, CallFlow(target=target))])

    # callsite instructions
    return instructions


def configure_callsites() -> GraphNode:
    return GraphNode(
        builder=patch_all_callsites,
        constraint=None,
        produces=("llvm/patches/callsites",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("instructions", "llvm/instructions"),
                ("entries", "llvm/functions/entries"),
            }
        ),
    )


def patch_all_callsites(
    generator: Generator,
    instructions: OneToMany[BlockId, BlockInstruction],
    entries: OneToOne[FunctionId, BlockId],
) -> OneToOne[FlowId, InstructionEntry]:
    calls: Dict[FlowId, InstructionEntry] = {}

    for batch in instructions.values():
        for fid, flow in batch:
            if isinstance(flow, CallFlow):
                # CallFlow is referenced by FlowId
                assert isinstance(fid, FlowId)

                calls[fid] = (
                    InstructionId(value=generator.next()),
                    Call(target=entries.get(flow.target)),
                )

    return OneToOne[FlowId, InstructionEntry].instance(calls)


def configure_clobbers_patching() -> GraphNode:
    return GraphNode(
        builder=patch_clobbers,
        constraint=None,
        produces=("llvm/patches/clobbers",),
        requires=frozenset(
            {
                ("generator", "core/generator"),
                ("blocks", "llvm/functions/blocks"),
                ("instructions", "llvm/instructions"),
            }
        ),
    )


def patch_clobbers(
    generator: Generator,
    blocks: OneToMany[FunctionId, BlockId],
    instructions: OneToMany[BlockId, BlockInstruction],
) -> OneToOne[FlowId, InstructionEntry]:
    bindings: Dict[FlowId, InstructionEntry] = {}

    for _, bids in blocks.items():
        for bid in bids:
            for iid, instr in instructions.get(bid):
                if not isinstance(iid, FlowId):
                    continue

                if isinstance(instr, ClobbersFlow):
                    # ClobbersFlow is referenced by FlowId
                    assert isinstance(iid, FlowId)

                    bindings[iid] = (InstructionId(value=generator.next()), Nop())

    return OneToOne[FlowId, InstructionEntry].instance(bindings)
