from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.indices.dataflows import DataFlowListExtractor
from i13c.semantic.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_dataflows():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn main(arg1: u8, arg2: u8) { foo(arg1); bar(arg2); }
    """)

    draw_list(DataFlowListExtractor, graph).equals("""
        | --------- | ----------- | ------------- | ---------------- | ----------------- | ------------- | -------------- |
        | Reference | Function ID | Function Name | ControlFlow Node | DataFlow Declares | DataFlow Uses | DataFlow Drops |
        | --------- | ----------- | ------------- | ---------------- | ----------------- | ------------- | -------------- |
        | 12:36     | function#1  | main          | callsite#4       | 0                 | 1             | 0              |
        | 12:36     | function#1  | main          | callsite#6       | 0                 | 1             | 0              |
        | 12:36     | function#1  | main          | entry#8          | 2                 | 0             | 0              |
        | 12:36     | function#1  | main          | exit#9           | 0                 | 0             | 2              |
        | --------- | ----------- | ------------- | ---------------- | ----------------- | ------------- | -------------- |
    """)
