from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.rules.semantic import SemanticListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_semantic_rules_summary():
    artifacts = prepare_artifacts("""
        fn main() { foo(0x123); }
    """)

    draw_list(SemanticListExtractor, artifacts).equals("""
        | --------- | --------- | --------------------------------------------------- |
        | Reference | Rule Code | Rule Message                                        |
        | --------- | --------- | --------------------------------------------------- |
        | 21:31     | E3008     | Called symbol does not exist: b'foo'                |
        |           | E3011     | Missing entrypoint function or snippet named 'main' |
        | --------- | --------- | --------------------------------------------------- |
    """)
