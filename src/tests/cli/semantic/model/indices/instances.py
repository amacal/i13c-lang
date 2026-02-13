from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.indices.instances import InstanceListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_instances():
    artifacts = prepare_artifacts("""
        asm exit(code@rax: u8) {}
        fn main() { exit(0x01); }
    """)

    draw_list(InstanceListExtractor, artifacts).equals("""
        | --------- | ----------- | ----------- | --------- | -------- | -------- |
        | Reference | Callsite ID | Callee Name | Target    | Bindings | Operands |
        | --------- | ----------- | ----------- | --------- | -------- | -------- |
        | 55:65     | callsite#3  | exit        | snippet#1 | 1        | 0        |
        | --------- | ----------- | ----------- | --------- | -------- | -------- |
    """)
