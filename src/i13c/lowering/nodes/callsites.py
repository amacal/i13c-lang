from typing import Dict, List, Set, Tuple

from i13c.core.dag import GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.nodes.bindings import lower_function_bindings, lower_snippet_bindings
from i13c.lowering.nodes.instances import lower_instance
from i13c.lowering.nodes.registers import IR_REGISTER_MAP
from i13c.lowering.typing.blocks import BlockInstruction
from i13c.lowering.typing.flows import (
    BlockId,
    CallFlow,
    FlowId,
    PreserveFlow,
    RestoreFlow,
)
from i13c.lowering.typing.instructions import Call, InstructionEntry, InstructionId
from i13c.semantic.model import SemanticGraph
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.snippets import SnippetId


def lower_callsite(
    graph: SemanticGraph,
    cid: CallSiteId,
) -> Tuple[List[BlockInstruction], Set[int]]:

    # prepare result containers
    clobbers: Set[int] = set()
    instructions: List[BlockInstruction] = []

    # retrieve callsite resolution
    resolution = graph.indices.resolution_by_callsite.get(cid)

    # we expected no ambiguity here
    assert len(resolution.accepted) == 1

    # append preserve instructions
    iid = FlowId(value=graph.generator.next())
    instructions.append((iid, PreserveFlow()))

    if isinstance(resolution.accepted[0].callable.target, SnippetId):
        instance = graph.indices.instance_by_callsite.get(cid)
        snippet = graph.basic.snippets.get(instance.target)

        # append callsite specific bindings
        instructions.extend(lower_snippet_bindings(graph, instance.bindings))

        # append emitted instructions
        instructions.extend(lower_instance(graph, instance))

        # update clobbered registers
        clobbers.update(
            [IR_REGISTER_MAP[register.name] for register in snippet.clobbers]
        )

    else:

        # extract bindings
        bindings = resolution.accepted[0].bindings

        # append callsite specific bindings
        instructions.extend(lower_function_bindings(graph, bindings))

        # extract successfully resolved target
        target = resolution.accepted[0].callable.target

        # append callsite call instructions
        iid = FlowId(value=graph.generator.next())
        instructions.extend([(iid, CallFlow(target=target))])

        # all IR registers are clobbered by function calls
        clobbers.update(set(IR_REGISTER_MAP.values()))

    # append restore instructions
    iid = FlowId(value=graph.generator.next())
    instructions.append((iid, RestoreFlow()))

    # callsite instructions and clobbers
    return instructions, clobbers


def configure_callsites() -> GraphNode:
    return GraphNode(
        builder=patch_all_callsites,
        constraint=None,
        produces=("llvm/patches/callsites",),
        requires=frozenset(
            {
                ("graph", "semantic/graph"),
                ("instructions", "llvm/blocks/instructions"),
                ("entries", "llvm/functions/entries"),
            }
        ),
    )


def patch_all_callsites(
    graph: SemanticGraph,
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
                    InstructionId(value=graph.generator.next()),
                    Call(target=entries.get(flow.target)),
                )

    return OneToOne[FlowId, InstructionEntry].instance(calls)
