from typing import Optional

from i13c.core.dag import GraphGroup, GraphNode
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.graph import LowLevelContext, LowLevelGraph
from i13c.lowering.nodes.bindings import patch_bindings
from i13c.lowering.nodes.blocks import emit_all_blocks, patch_registers
from i13c.lowering.nodes.callsites import patch_all_callsites
from i13c.lowering.nodes.functions import configure_functions
from i13c.lowering.nodes.stacks import patch_stack_frames
from i13c.lowering.typing.blocks import Block
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.instructions import Instruction
from i13c.semantic.model import SemanticGraph
from i13c.semantic.rules import SemanticRules
from i13c.semantic.typing.entities.functions import FunctionId


def build_low_level_graph(
    graph: SemanticGraph,
    entrypoint: BlockId,
    blocks: OneToOne[BlockId, Block],
    forward: OneToMany[BlockId, BlockId],
    backward: OneToMany[BlockId, BlockId],
    entries: OneToOne[FunctionId, BlockId],
    exits: OneToOne[FunctionId, BlockId],
) -> LowLevelGraph:
    # a backward compatible context
    ctx = LowLevelContext(
        graph=graph,
        generator=graph.generator,
        nodes=blocks.data,
        forward=forward.data,
        backward=backward.data,
        entry=entries.data,
        exit=exits.data,
        flows={},
        stack={},
        values={},
    )

    # some bindings are still unresolved
    # we need to lower expressions into instructions
    patch_bindings(ctx)

    # some callsites still contain not resolved calls
    # we need to map FunctionId to BlockId
    patch_all_callsites(ctx)

    # each block must maintain alive registers
    # this is required for correct register allocation
    patch_registers(ctx)

    # all prologues/epilogues must have stack frames assigned
    # currently they are only initialized as flows
    patch_stack_frames(ctx)

    # each block now can be linearized independently
    # connection between blocks is already known
    emit_all_blocks(ctx, entrypoint)

    # materialize low-level graph
    return LowLevelGraph(
        entry=entrypoint,
        nodes=OneToOne[BlockId, Block].instance(ctx.nodes),
        forward=OneToMany[BlockId, BlockId].instance(ctx.forward),
        backward=OneToMany[BlockId, BlockId].instance(ctx.backward),
        flows=OneToMany[BlockId, Instruction].instance(ctx.flows),
    )


def configure_llvm_graph() -> GraphGroup:
    graph = GraphNode(
        builder=build,
        produces=("llvm/graph",),
        requires=frozenset(
            {
                ("graph", "semantic/graph"),
                ("rules", "rules/semantic"),
                ("entrypoint", "llvm/entrypoint"),
                ("blocks", "llvm/blocks"),
                ("forward", "llvm/forward"),
                ("backward", "llvm/backward"),
                ("entries", "llvm/entries"),
                ("exits", "llvm/exits"),
            }
        ),
    )

    return GraphGroup(nodes=[graph, configure_functions()])


def build(
    graph: SemanticGraph,
    rules: SemanticRules,
    entrypoint: BlockId,
    blocks: OneToOne[BlockId, Block],
    forward: OneToMany[BlockId, BlockId],
    backward: OneToMany[BlockId, BlockId],
    entries: OneToOne[FunctionId, BlockId],
    exits: OneToOne[FunctionId, BlockId],
) -> Optional[LowLevelGraph]:

    # prevent lowering if there are any semantic errors
    if rules.count() > 0:
        return None

    return build_low_level_graph(
        graph, entrypoint, blocks, forward, backward, entries, exits
    )
