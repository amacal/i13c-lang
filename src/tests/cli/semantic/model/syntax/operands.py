from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.syntax.operands import OperandListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_operands():
    artifacts = prepare_artifacts("""
        asm main(abc@rbx: u64) { mov rax, abc; }
    """)

    draw_list(OperandListExtractor, artifacts).equals("""
        | --------- | ------- | ------------ | ------------- | --------------- | -------------- |
        | Reference | Node ID | Operand Kind | Register Name | Immediate Value | Reference Name |
        | --------- | ------- | ------------ | ------------- | --------------- | -------------- |
        | 38:41     | #3      | register     | rax           |                 |                |
        | 43:46     | #4      | reference    |               |                 | abc            |
        | --------- | ------- | ------------ | ------------- | --------------- | -------------- |
    """)
