from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.indices.terminalities import TerminalityListExtractor
from i13c.sem.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_terminalities():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn main() noreturn { }
    """)

    draw_list(TerminalityListExtractor, graph).equals("""
        | --------- | ----------- | ------------- | ----------------- | -------------------- |
        | Reference | Function ID | Function Name | Function NoReturn | Terminality NoReturn |
        | --------- | ----------- | ------------- | ----------------- | -------------------- |
        | 12:18     | function#1  | main          | true              | false                |
        | --------- | ----------- | ------------- | ----------------- | -------------------- |
    """)
