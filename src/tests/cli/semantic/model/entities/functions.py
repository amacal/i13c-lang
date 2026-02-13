from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.functions import FunctionListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_functions():
    artifacts = prepare_artifacts("""
        fn main() { }
    """)

    draw_list(FunctionListExtractor, artifacts).equals("""
        | --------- | ----------- | ------------- | --------- | ---------- | ---------- |
        | Reference | Function ID | Function Name | No Return | Parameters | Statements |
        | --------- | ----------- | ------------- | --------- | ---------- | ---------- |
        | 12:18     | function#1  | main          | false     | 0          | 0          |
        | --------- | ----------- | ------------- | --------- | ---------- | ---------- |
    """)
