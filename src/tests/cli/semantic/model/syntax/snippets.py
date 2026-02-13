from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.syntax.snippets import SnippetListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_snippets():
    artifacts = prepare_artifacts("""
        asm main(code@rbx: u64) clobbers rax, rbx { mov rax, rbx; }
    """)

    draw_list(SnippetListExtractor, artifacts).equals("""
        | --------- | ------- | ------------ | ----- | -------- | ------------ |
        | Reference | Node ID | Snippet Name | Slots | Clobbers | Instructions |
        | --------- | ------- | ------------ | ----- | -------- | ------------ |
        | 13:32     | #1      | main         | 1     | 2        | 1            |
        | --------- | ------- | ------------ | ----- | -------- | ------------ |
    """)
