from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.syntax.parameters import ParameterListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_parameters():
    artifacts = prepare_artifacts("""
        fn main(abc: u8[0x01..0x02], cde: u64) { }
    """)

    draw_list(ParameterListExtractor, artifacts).equals("""
        | --------- | ------- | -------------- | -------------- | --------------- |
        | Reference | Node ID | Parameter Name | Parameter Type | Parameter Range |
        | --------- | ------- | -------------- | -------------- | --------------- |
        | 17:20     | #2      | abc            | u8             | 0x0001..0x0002  |
        | 38:41     | #3      | cde            | u64            |                 |
        | --------- | ------- | -------------- | -------------- | --------------- |
    """)
