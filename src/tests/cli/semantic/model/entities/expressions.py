from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.expressions import ExpressionListExtractor
from i13c.sem.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_expressions():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn main(abc: u8) { foo(abc); }
    """)

    draw_list(ExpressionListExtractor, graph).equals("""
        | --------- | ------------- | --------------- |
        | Reference | Expression ID | Expression Name |
        | --------- | ------------- | --------------- |
        | 32:35     | expression#4  | abc             |
        | --------- | ------------- | --------------- |
    """)
