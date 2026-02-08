from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.literals import LiteralListExtractor
from i13c.semantic.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_literals():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn main() { foo(0x123); }
    """)

    draw_list(LiteralListExtractor, graph).equals("""
        | --------- | ---------- | ------------ | --------- | --------- |
        | Reference | Literal ID | Literal Kind | Hex Value | Hex Width |
        | --------- | ---------- | ------------ | --------- | --------- |
        | 25:30     | literal#3  | hex          | 291       | 16        |
        | --------- | ---------- | ------------ | --------- | --------- |
    """)
