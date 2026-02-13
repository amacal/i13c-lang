from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.parameters import ParameterListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_parameters():
    artifacts = prepare_artifacts("""
        fn main(abc: u8[0x01..0x02], cde: u64) { }
    """)

    draw_list(ParameterListExtractor, artifacts).equals("""
        | --------- | ------------ | -------------- | ---------------------------- |
        | Reference | Parameter ID | Parameter Name | Parameter Type               |
        | --------- | ------------ | -------------- | ---------------------------- |
        | 17:20     | parameter#2  | abc            | u8[1..2]                     |
        | 38:41     | parameter#3  | cde            | u64[0..18446744073709551615] |
        | --------- | ------------ | -------------- | ---------------------------- |
    """)
