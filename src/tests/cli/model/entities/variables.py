from i13c.cli.model import draw_list
from i13c.cli.model.entities.variables import VariableListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_variables():
    artifacts = prepare_artifacts("""
        fn main(abc: u8[0x01..0x02], cde: u64) { }
    """)

    draw_list(VariableListExtractor, artifacts).equals("""
        | --------- | ----------- | ------------- | ------------------------------------------- | ------------- | --------------- |
        | Reference | Variable ID | Variable Name | Variable Type                               | Variable Kind | Variable Source |
        | --------- | ----------- | ------------- | ------------------------------------------- | ------------- | --------------- |
        | 17:20     | variable#2  | abc           | u8[0x01..0x02]                              | parameter     | parameter#2     |
        | 38:41     | variable#5  | cde           | u64[0x0000000000000000..0xffffffffffffffff] | parameter     | parameter#5     |
        | --------- | ----------- | ------------- | ------------------------------------------- | ------------- | --------------- |
    """)
