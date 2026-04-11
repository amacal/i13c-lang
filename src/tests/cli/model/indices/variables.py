from i13c.cli.model import draw_list
from i13c.cli.model.indices.variables import ParameterVariablesListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_parameter_variables():
    artifacts = prepare_artifacts(
        """
            fn main(arg1: u8, arg2: u16) { foo(arg1); bar(arg2); }
        """
    )

    draw_list(ParameterVariablesListExtractor, artifacts).equals(
        """
            | --------- | ----------- | ----------- | ----------- |
            | Reference | Source ID   | Source Name | Variable ID |
            | --------- | ----------- | ----------- | ----------- |
            | 21:29     | parameter#2 | arg1        | variable#2  |
            | 31:40     | parameter#4 | arg2        | variable#4  |
            | --------- | ----------- | ----------- | ----------- |
        """
    )
