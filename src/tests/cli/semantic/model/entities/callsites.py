from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.callsites import CallSiteListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_callsites():
    artifacts = prepare_artifacts("""
        fn main() { foo(0x123); }
    """)

    draw_list(CallSiteListExtractor, artifacts).equals("""
        | --------- | ----------- | ----------- | --------- |
        | Reference | Callsite ID | Callee Name | Arguments |
        | --------- | ----------- | ----------- | --------- |
        | 21:31     | callsite#2  | foo         | 1         |
        | --------- | ----------- | ----------- | --------- |
    """)
