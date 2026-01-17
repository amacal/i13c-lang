from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.graph import LowLevelContext, LowLevelGraph
from i13c.lowering.linear import emit_all_blocks
from i13c.lowering.nodes.callsites import patch_all_callsites
from i13c.lowering.nodes.functions import lower_active_functions
from i13c.lowering.typing.blocks import Block
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.instructions import Instruction
from i13c.sem.model import SemanticGraph


def build_low_level_graph(graph: SemanticGraph) -> LowLevelGraph:
    ctx = LowLevelContext.empty(graph)

    # lower all active functions in any order
    # also obtain entrypoint of the program
    entry = lower_active_functions(ctx)

    # some callsites still contain not resolved calls
    # we need to map FunctionId to BlockId
    patch_all_callsites(ctx)

    # each block now can be linearized independently
    # connection between blocks is already known
    emit_all_blocks(ctx, entry)

    # materialize low-level graph
    return LowLevelGraph(
        entry=entry,
        nodes=OneToOne[BlockId, Block].instance(ctx.nodes),
        edges=OneToMany[BlockId, BlockId].instance(ctx.edges),
        flows=OneToMany[BlockId, Instruction].instance(ctx.flows),
    )
