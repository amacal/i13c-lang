from typing import Any, Dict

from i13c.core.dag import GraphGroup, GraphNode, Prefix
from i13c.core.mapping import OneToMany, OneToOne
from i13c.llvm.graph import (
    BlockRegistersNode,
    FunctionsNode,
    InstructionRegistersNode,
    LowLevelGraph,
    PatchesNode,
)
from i13c.llvm.nodes.bindings import configure_binding_patching
from i13c.llvm.nodes.blocks import (
    configure_defined_and_used_registers_for_blocks,
    configure_defined_and_used_registers_for_instructions,
    configure_function_blocks,
    configure_function_instructions,
    configure_in_and_out_registers_for_blocks,
    configure_in_and_out_registers_for_instructions,
    configure_instruction_emission,
    configure_register_interval_pressure,
    configure_register_intervals,
)
from i13c.llvm.nodes.callsites import (
    configure_callsites,
    configure_clobbers_patching,
)
from i13c.llvm.nodes.functions import (
    configure_functions,
    configure_snapshot_patching,
)
from i13c.llvm.nodes.registers import configure_registers
from i13c.llvm.nodes.stacks import configure_stack_frames, configure_stack_patching
from i13c.llvm.typing.blocks import BlockInstruction, BlockInstructionId, Registers
from i13c.llvm.typing.flows import BlockId
from i13c.llvm.typing.instructions import Instruction
from i13c.llvm.typing.registers import VirtualRegister
from i13c.semantic.typing.indices.variables import VariableId


def configure_llvm_graph() -> GraphGroup:
    return GraphGroup(
        nodes=[
            configure_self(),
            configure_functions(),
            configure_callsites(),
            configure_registers(),
            configure_clobbers_patching(),
            configure_binding_patching(),
            configure_snapshot_patching(),
            configure_stack_patching(),
            configure_stack_frames(),
            configure_function_blocks(),
            configure_register_intervals(),
            configure_function_instructions(),
            configure_register_interval_pressure(),
            configure_defined_and_used_registers_for_blocks(),
            configure_defined_and_used_registers_for_instructions(),
            configure_in_and_out_registers_for_blocks(),
            configure_in_and_out_registers_for_instructions(),
            configure_instruction_emission(),
            # configure_used_registers_computation(),
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
                ("flows", "llvm/instructions"),
                ("instructions", "assembler/instructions"),
                ("functions", Prefix(value="llvm/functions/")),
                ("blocks", Prefix(value="llvm/blocks")),
                ("patches", Prefix(value="llvm/patches/")),
                ("registers", "llvm/registers"),
                ("iregs", Prefix(value="llvm/instructions/registers/")),
                ("bregs", Prefix(value="llvm/blocks/registers/")),
            }
        ),
    )


def build(
    entrypoint: BlockId,
    blocks: Dict[str, Any],
    flows: OneToMany[BlockId, BlockInstruction],
    instructions: OneToMany[BlockId, Instruction],
    functions: Dict[str, Any],
    patches: Dict[str, Any],
    iregs: Dict[str, OneToOne[BlockInstructionId, Registers]],
    bregs: Dict[str, OneToOne[BlockId, Registers]],
    registers: OneToOne[VariableId, VirtualRegister],
) -> LowLevelGraph:
    return LowLevelGraph(
        entry=entrypoint,
        nodes=blocks["llvm/blocks"],
        flows=flows,
        instructions=instructions,
        forward=blocks["llvm/blocks/forward"],
        backward=blocks["llvm/blocks/backward"],
        registers=registers,
        functions=FunctionsNode(
            entries=functions["llvm/functions/entries"],
            exits=functions["llvm/functions/exits"],
            blocks=functions["llvm/functions/blocks"],
            stacks=functions["llvm/functions/stackframes"],
            intervals=functions["llvm/functions/intervals"],
            pressures=functions["llvm/functions/intervals/pressure"],
            instructions=functions["llvm/functions/instructions"],
        ),
        patches=PatchesNode(
            clobbers=patches["llvm/patches/clobbers"],
            stackframes=patches["llvm/patches/stacks"],
            bindings=patches["llvm/patches/bindings"],
            callsites=patches["llvm/patches/callsites"],
            snapshots=patches["llvm/patches/snapshots"],
        ),
        iregs=InstructionRegistersNode(
            used=iregs["llvm/instructions/registers/use"],
            inputs=iregs["llvm/instructions/registers/in"],
            outputs=iregs["llvm/instructions/registers/out"],
            clobbers=OneToOne[BlockInstructionId, Registers].instance({}),
            generated=iregs["llvm/instructions/registers/def"],
        ),
        bregs=BlockRegistersNode(
            used=bregs["llvm/blocks/registers/use"],
            inputs=bregs["llvm/blocks/registers/in"],
            outputs=bregs["llvm/blocks/registers/out"],
            clobbers=OneToOne[BlockId, Registers].instance({}),
            generated=bregs["llvm/blocks/registers/def"],
        ),
    )
