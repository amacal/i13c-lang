from i13c.cli.model import draw_list
from i13c.cli.model.entities.literals import LiteralListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_literals():
    artifacts = prepare_artifacts("""
        fn main() { foo(0x0123); }
    """)

    draw_list(LiteralListExtractor, artifacts).equals("""
        | --------- | ---------- | ------------ | --------- | --------- |
        | Reference | Literal ID | Literal Kind | Hex Value | Hex Width |
        | --------- | ---------- | ------------ | --------- | --------- |
        | 25:31     | literal#3  | hex          | 0x0123    | 16        |
        | --------- | ---------- | ------------ | --------- | --------- |
    """)
