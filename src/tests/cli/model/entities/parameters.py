from i13c.cli.model import draw_list
from i13c.cli.model.entities.parameters import ParameterListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_parameters():
    artifacts = prepare_artifacts("""
        fn main(abc: u8[0x01..0x02], cde: u64) { }
    """)

    draw_list(ParameterListExtractor, artifacts).equals("""
        | --------- | ------------ | -------------- | ------------------------------------------- |
        | Reference | Parameter ID | Parameter Name | Parameter Type                              |
        | --------- | ------------ | -------------- | ------------------------------------------- |
        | 17:20     | parameter#2  | abc            | u8[0x01..0x02]                              |
        | 38:41     | parameter#5  | cde            | u64[0x0000000000000000..0xffffffffffffffff] |
        | --------- | ------------ | -------------- | ------------------------------------------- |
    """)
