from i13c.lowering.graph import LowLevelContext
from i13c.lowering.nodes.blocks import linearize_blocks
from i13c.lowering.typing.flows import (
    EpilogueFlow,
    PreserveFlow,
    PrologueFlow,
    RestoreFlow,
)
from i13c.lowering.typing.instructions import (
    EnterFrame,
    ExitFrame,
    Preserve,
    Restore,
)
from i13c.lowering.typing.stacks import StackFrame


def patch_stack_frames(ctx: LowLevelContext) -> None:
    # first determine all stack frame
    for fid in ctx.entry.keys():
        # initialize maximum preserved size
        preserves = 0

        # analyze function blocks for stack usage
        for bid in linearize_blocks(ctx.entry[fid], ctx.forward):
            block = ctx.nodes[bid]
            registers = block.registers.inputs - block.registers.outputs
            preserves = max(preserves, 8 * len(registers))

        # determine stack frame for function
        ctx.stack[fid] = StackFrame(size=preserves)

    # then patch all prologues/epilogues
    for block in ctx.nodes.values():
        for idx, instruction in enumerate(block.instructions):
            if isinstance(instruction, PrologueFlow):
                stackframe = ctx.stack[instruction.target]
                block.instructions[idx] = EnterFrame(size=stackframe.size)

            if isinstance(instruction, EpilogueFlow):
                stackframe = ctx.stack[instruction.target]
                block.instructions[idx] = ExitFrame(size=stackframe.size)

            if isinstance(instruction, PreserveFlow):
                # determine affected registers
                registers = block.registers.inputs - block.registers.outputs

                # generate preserve instruction
                block.instructions[idx] = Preserve(
                    registers={idx: reg for idx, reg in enumerate(sorted(registers))}
                )

            if isinstance(instruction, RestoreFlow):
                # determine affected registers
                registers = block.registers.inputs - block.registers.outputs

                # generate restore instruction
                block.instructions[idx] = Restore(
                    registers={idx: reg for idx, reg in enumerate(sorted(registers))}
                )
