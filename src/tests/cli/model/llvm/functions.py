from i13c.cli.model import draw_list
from i13c.cli.model.llvm.functions import EntriesListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_function_entries():
    artifacts = prepare_artifacts("""
        asm exit() noreturn { syscall; }
        fn main() noreturn { exit(); }
    """)

    draw_list(EntriesListExtractor, artifacts).equals("""
        | ----------- | ------------- | -------- | ------------- |
        | Function ID | Function Name | Block ID | Terminator    |
        | ----------- | ------------- | -------- | ------------- |
        | function#3  | main          | block#8  | Jump(block#7) |
        | ----------- | ------------- | -------- | ------------- |
    """)
