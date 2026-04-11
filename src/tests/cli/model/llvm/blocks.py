from i13c.cli.model import draw_list
from i13c.cli.model.llvm.blocks import (
    BlockInstructionsListExtractor,
    BlockListExtractor,
)
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_blocks():
    artifacts = prepare_artifacts(
        """
            asm exit() noreturn { syscall; }
            fn main() noreturn { exit(); }
        """
    )

    draw_list(BlockListExtractor, artifacts).equals(
        """
            | -------- | ---------- | ------------- |
            | Block ID | Origin     | Terminator    |
            | -------- | ---------- | ------------- |
            | block#8  | function#4 | Jump(block#9) |
            | block#9  | callsite#5 | Trap          |
            | -------- | ---------- | ------------- |
        """
    )


def can_draw_a_table_with_block_instructions():
    artifacts = prepare_artifacts(
        """
            asm exit() noreturn { syscall; }
            fn main() noreturn { exit(); }
        """
    )

    draw_list(BlockInstructionsListExtractor, artifacts).equals(
        """
            | -------- | ---------- | ----- | ----------- | ------------------- |
            | Block ID | Origin     | Index | Kind        | Instruction         |
            | -------- | ---------- | ----- | ----------- | ------------------- |
            | block#8  | function#4 | 0     | flow        | prologue function#4 |
            | block#9  | callsite#5 | 0     | instruction | syscall             |
            | -------- | ---------- | ----- | ----------- | ------------------- |
        """
    )
