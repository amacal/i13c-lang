from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.indices.terminalities import TerminalityListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_terminalities():
    artifacts = prepare_artifacts("""
        fn main() noreturn { }
    """)

    draw_list(TerminalityListExtractor, artifacts).equals("""
        | --------- | ----------- | ------------- | ----------------- | -------------------- |
        | Reference | Function ID | Function Name | Function NoReturn | Terminality NoReturn |
        | --------- | ----------- | ------------- | ----------------- | -------------------- |
        | 12:18     | function#1  | main          | true              | false                |
        | --------- | ----------- | ------------- | ----------------- | -------------------- |
    """)
