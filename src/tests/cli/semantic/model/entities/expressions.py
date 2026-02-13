from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.expressions import ExpressionListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_expressions():
    artifacts = prepare_artifacts("""
        fn main(abc: u8) { foo(abc); }
    """)

    draw_list(ExpressionListExtractor, artifacts).equals("""
        | --------- | ------------- | --------------- |
        | Reference | Expression ID | Expression Name |
        | --------- | ------------- | --------------- |
        | 32:35     | expression#4  | abc             |
        | --------- | ------------- | --------------- |
    """)
