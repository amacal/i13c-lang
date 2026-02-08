from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.callsites import CallSiteListExtractor
from i13c.sem.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_callsites():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn main() { foo(0x123); }
    """)

    draw_list(CallSiteListExtractor, graph).equals("""
        | --------- | ----------- | ----------- | --------- |
        | Reference | Callsite ID | Callee Name | Arguments |
        | --------- | ----------- | ----------- | --------- |
        | 21:31     | callsite#2  | foo         | 1         |
        | --------- | ----------- | ----------- | --------- |
    """)
