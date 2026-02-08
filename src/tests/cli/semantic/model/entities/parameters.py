from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.parameters import ParameterListExtractor
from i13c.sem.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_parameters():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn main(abc: u8[0x01..0x02], cde: u64) { }
    """)

    draw_list(ParameterListExtractor, graph).equals("""
        | --------- | ------------ | -------------- | ---------------------------- |
        | Reference | Parameter ID | Parameter Name | Parameter Type               |
        | --------- | ------------ | -------------- | ---------------------------- |
        | 17:20     | parameter#2  | abc            | u8[1..2]                     |
        | 38:41     | parameter#3  | cde            | u64[0..18446744073709551615] |
        | --------- | ------------ | -------------- | ---------------------------- |
    """)
