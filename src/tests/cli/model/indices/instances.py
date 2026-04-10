from i13c.cli.model import draw_list
from i13c.cli.model.indices.instances import InstanceListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_instances():
    artifacts = prepare_artifacts(
        """
            asm exit(code@rax: u8) {}
            fn main() { exit(0x01); }
        """
    )

    draw_list(InstanceListExtractor, artifacts).equals(
        """
            | --------- | ----------- | ----------- | --------- | -------- | -------- |
            | Reference | Callsite ID | Callee Name | Target    | Bindings | Operands |
            | --------- | ----------- | ----------- | --------- | -------- | -------- |
            | 63:73     | callsite#5  | exit        | snippet#1 | 1        | 0        |
            | --------- | ----------- | ----------- | --------- | -------- | -------- |
        """
    )
