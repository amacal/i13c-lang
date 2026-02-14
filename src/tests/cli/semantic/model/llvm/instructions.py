from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.llvm.instructions import InstructionsListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_instructions():
    artifacts = prepare_artifacts("""
        asm exit() noreturn { syscall; }
        fn main() noreturn { exit(); }
    """)

    draw_list(InstructionsListExtractor, artifacts).equals("""
        | -------- | ---------- | ----- | ----------------------- |
        | Block ID | Origin     | Index | Instruction             |
        | -------- | ---------- | ----- | ----------------------- |
        | block#8  | function#3 | 0     | SubRegImm(dst=4, imm=0) |
        | block#8  | function#3 | 1     | SysCall()               |
        | -------- | ---------- | ----- | ----------------------- |
    """)
