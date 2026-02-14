from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.llvm.blocks import (
    BlockInstructionsListExtractor,
    BlockListExtractor,
)
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_blocks():
    artifacts = prepare_artifacts("""
        asm exit() noreturn { syscall; }
        fn main() noreturn { exit(); }
    """)

    draw_list(BlockListExtractor, artifacts).equals("""
        | -------- | ---------- | ------------- | ------------ |
        | Block ID | Origin     | Terminator    | Instructions |
        | -------- | ---------- | ------------- | ------------ |
        | block#7  | callsite#4 | Trap          | 3            |
        | block#8  | function#3 | Jump(block#7) | 1            |
        | -------- | ---------- | ------------- | ------------ |
    """)


def can_draw_a_table_with_block_instructions():
    artifacts = prepare_artifacts("""
        asm exit() noreturn { syscall; }
        fn main() noreturn { exit(); }
    """)

    draw_list(BlockInstructionsListExtractor, artifacts).equals("""
        | -------- | ---------- | ----- | ----------- | ---------------------- |
        | Block ID | Origin     | Index | Kind        | Instruction            |
        | -------- | ---------- | ----- | ----------- | ---------------------- |
        | block#7  | callsite#4 | 0     | abstract    | Preserve(registers={}) |
        | block#7  | callsite#4 | 1     | instruction | SysCall()              |
        | block#7  | callsite#4 | 2     | abstract    | Restore(registers={})  |
        | block#8  | function#3 | 0     | abstract    | EnterFrame(size=0)     |
        | -------- | ---------- | ----- | ----------- | ---------------------- |
    """)
