from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.syntax.literals import (
    LiteralIntegersListExtractor,
    LiteralListExtractor,
)
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_literals():
    artifacts = prepare_artifacts("""
        fn main() { foo(0x123); }
    """)

    draw_list(LiteralListExtractor, artifacts).equals("""
        | --------- | ------- | -------------- |
        | Reference | Node ID | Literal Kind   |
        | --------- | ------- | -------------- |
        | 25:30     | #3      | IntegerLiteral |
        | --------- | ------- | -------------- |
    """)


def can_draw_a_table_with_integer_literals():
    artifacts = prepare_artifacts("""
        fn main() { foo(0x123); }
    """)

    draw_list(LiteralIntegersListExtractor, artifacts).equals("""
        | --------- | ------- | ------------- |
        | Reference | Node ID | Integer Value |
        | --------- | ------- | ------------- |
        | 25:30     | #3      | 291           |
        | --------- | ------- | ------------- |
    """)
