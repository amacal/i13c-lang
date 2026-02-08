from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.variables import VariableListExtractor
from i13c.semantic.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_variables():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn main(abc: u8[0x01..0x02], cde: u64) { }
    """)

    draw_list(VariableListExtractor, graph).equals("""
        | --------- | ----------- | ------------- | ---------------------------- | ------------- | --------------- |
        | Reference | Variable ID | Variable Name | Variable Type                | Variable Kind | Variable Source |
        | --------- | ----------- | ------------- | ---------------------------- | ------------- | --------------- |
        | 17:20     | variable#2  | abc           | u8[1..2]                     | parameter     | parameter#2     |
        | 38:41     | variable#3  | cde           | u64[0..18446744073709551615] | parameter     | parameter#3     |
        | --------- | ----------- | ------------- | ---------------------------- | ------------- | --------------- |
    """)
