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
        | -------- | ---------- | ------------- |
        | Block ID | Origin     | Terminator    |
        | -------- | ---------- | ------------- |
        | block#7  | callsite#4 | Trap          |
        | block#8  | function#3 | Jump(block#7) |
        | -------- | ---------- | ------------- |
    """)


def can_draw_a_table_with_block_instructions():
    artifacts = prepare_artifacts("""
        asm exit() noreturn { syscall; }
        fn main() noreturn { exit(); }
    """)

    draw_list(BlockInstructionsListExtractor, artifacts).equals("""
        | -------- | ---------- | ----- | ----------- | ------------------- |
        | Block ID | Origin     | Index | Kind        | Instruction         |
        | -------- | ---------- | ----- | ----------- | ------------------- |
        | block#7  | callsite#4 | 0     | flow        | preserve            |
        | block#7  | callsite#4 | 1     | instruction | syscall             |
        | block#7  | callsite#4 | 2     | flow        | restore             |
        | block#8  | function#3 | 0     | flow        | prologue function#3 |
        | -------- | ---------- | ----- | ----------- | ------------------- |
    """)
