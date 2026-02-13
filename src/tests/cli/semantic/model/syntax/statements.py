from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.syntax.statements import (
    StatementCallsListExtractor,
    StatementListExtractor,
)
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_statements():
    artifacts = prepare_artifacts("""
        fn main() { foo(0x123); }
    """)

    draw_list(StatementListExtractor, artifacts).equals("""
        | --------- | ------- | -------------- |
        | Reference | Node ID | Statement Kind |
        | --------- | ------- | -------------- |
        | 21:31     | #2      | CallStatement  |
        | --------- | ------- | -------------- |
    """)


def can_draw_a_table_with_statement_calls():
    artifacts = prepare_artifacts("""
        fn main() { foo(0x123); }
    """)

    draw_list(StatementCallsListExtractor, artifacts).equals("""
        | --------- | ------- | ------ | --------- |
        | Reference | Node ID | Callee | Arguments |
        | --------- | ------- | ------ | --------- |
        | 21:31     | #2      | foo    | 1         |
        | --------- | ------- | ------ | --------- |
    """)
