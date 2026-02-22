from typing import Any, Dict

from i13c.core.dag import GraphGroup, GraphNode, Prefix
from i13c.core.mapping import OneToMany, OneToOne
from i13c.lowering.graph import FunctionsNode, LowLevelGraph, RegistersNode
from i13c.lowering.nodes.bindings import configure_binding_patching
from i13c.lowering.nodes.blocks import (
    configure_instruction_emission,
    configure_register_patching,
)
from i13c.lowering.nodes.callsites import configure_callsites
from i13c.lowering.nodes.functions import configure_functions
from i13c.lowering.nodes.stacks import configure_stack_patching
from i13c.lowering.typing.blocks import BlockInstruction, Registers
from i13c.lowering.typing.flows import BlockId
from i13c.lowering.typing.instructions import Instruction
from i13c.semantic.typing.entities.functions import FunctionId


def configure_llvm_graph() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_self(),
            configure_functions(),
            configure_callsites(),
            configure_binding_patching(),
            configure_stack_patching(),
            configure_register_patching(),
            configure_instruction_emission(),
        ]
    )


def configure_self() -> GraphNode:
    return GraphNode(
        builder=build,
        constraint=None,
        produces=("llvm/graph",),
        requires=frozenset(
            {
                ("entrypoint", "llvm/entrypoint"),
                ("flows", "llvm/blocks/instructions"),
                ("instructions", "llvm/instructions"),
                ("functions", Prefix(value="llvm/functions/")),
                ("blocks", Prefix(value="llvm/blocks")),
                ("patches", Prefix(value="llvm/patches/")),
                ("registers", Prefix(value="llvm/registers/")),
            }
        ),
    )


def build(
    entrypoint: BlockId,
    blocks: Dict[str, Any],
    flows: OneToMany[BlockId, BlockInstruction],
    instructions: OneToMany[BlockId, Instruction],
    functions: Dict[str, OneToOne[FunctionId, BlockId]],
    patches: Dict[str, Any],
    registers: Dict[str, OneToOne[BlockId, Registers]],
) -> LowLevelGraph:
    return LowLevelGraph(
        entry=entrypoint,
        nodes=blocks["llvm/blocks"],
        flows=flows,
        instructions=instructions,
        forward=blocks["llvm/blocks/forward"],
        backward=blocks["llvm/blocks/backward"],
        functions=FunctionsNode(
            entries=functions["llvm/functions/entries"],
            exits=functions["llvm/functions/exits"],
        ),
        registers=RegistersNode(
            inputs=registers["llvm/registers/inputs"],
            outputs=registers["llvm/registers/outputs"],
            clobbers=registers["llvm/registers/clobbers"],
        ),
    )
