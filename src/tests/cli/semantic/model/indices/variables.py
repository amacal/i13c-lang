from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.indices.variables import ParameterVariablesListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_parameter_variables():
    artifacts = prepare_artifacts("""
        fn main(arg1: u8, arg2: u16) { foo(arg1); bar(arg2); }
    """)

    draw_list(ParameterVariablesListExtractor, artifacts).equals("""
        | --------- | ------------ | -------------- | ----------- |
        | Reference | Parameter ID | Parameter Name | Variable ID |
        | --------- | ------------ | -------------- | ----------- |
        | 17:21     | parameter#2  | arg1           | variable#2  |
        | 27:31     | parameter#3  | arg2           | variable#3  |
        | --------- | ------------ | -------------- | ----------- |
    """)
