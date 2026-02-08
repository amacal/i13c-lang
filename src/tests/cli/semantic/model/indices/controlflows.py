from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.indices.controlflows import ControlFlowListExtractor
from i13c.semantic.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_controlflows():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn main() { foo(); bar(); }
    """)

    draw_list(ControlFlowListExtractor, graph).equals("""
        | --------- | ----------- | ------------- | ----- | ----- |
        | Reference | Function ID | Function Name | Nodes | Edges |
        | --------- | ----------- | ------------- | ----- | ----- |
        | 12:18     | function#1  | main          | 4     | 3     |
        | --------- | ----------- | ------------- | ----- | ----- |
    """)
