from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.functions import FunctionListExtractor
from i13c.sem.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_functions():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn main() { }
    """)

    draw_list(FunctionListExtractor, graph).equals("""
        | --------- | ----------- | ------------- | ---------- | ---------- |
        | Reference | Function ID | Function Name | Parameters | Statements |
        | --------- | ----------- | ------------- | ---------- | ---------- |
        | 12:18     | function#1  | main          | 0          | 0          |
        | --------- | ----------- | ------------- | ---------- | ---------- |
    """)
