from i13c.cli.model import draw_list
from i13c.cli.model.syntax.parameters import ParameterListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_parameters():
    artifacts = prepare_artifacts(
        """
            fn main(abc: u8[0x01..0x02], cde: u64) { }
        """
    )

    draw_list(ParameterListExtractor, artifacts).equals(
        """
            | --------- | ------- | -------------- | -------------- | --------------- |
            | Reference | Node ID | Parameter Name | Parameter Type | Parameter Range |
            | --------- | ------- | -------------- | -------------- | --------------- |
            | 21:40     | #2      | abc            | u8             | 0x01..0x02      |
            | 42:50     | #5      | cde            | u64            |                 |
            | --------- | ------- | -------------- | -------------- | --------------- |
        """
    )
