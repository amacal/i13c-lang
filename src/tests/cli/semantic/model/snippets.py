from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.snippets import SnippetListExtractor
from i13c.sem.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_snippets():
    graph: SemanticGraph = prepare_semantic_graph("""
        asm main(code@rbx: u64) clobbers rax, rbx { mov rax, rbx; }
    """)

    draw_list(SnippetListExtractor, graph).equals("""
        | --------- | ---------- | ------------ | ----- | -------- | ------------ |
        | Reference | Snippet ID | Snippet Name | Slots | Clobbers | Instructions |
        | --------- | ---------- | ------------ | ----- | -------- | ------------ |
        | 13:32     | snippet#1  | main         | 1     | 2        | 1            |
        | --------- | ---------- | ------------ | ----- | -------- | ------------ |
    """)
