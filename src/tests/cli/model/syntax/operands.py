from i13c.cli.model import draw_list
from i13c.cli.model.syntax.operands import OperandListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_operands():
    artifacts = prepare_artifacts(
        """
            asm main(abc@rbx: u64) { mov rax, @abc; }
        """
    )

    draw_list(OperandListExtractor, artifacts).equals(
        """
            | --------- | ------- | ------------ | ------------- | --------------- | -------------- |
            | Reference | Node ID | Operand Kind | Register Name | Immediate Value | Reference Name |
            | --------- | ------- | ------------ | ------------- | --------------- | -------------- |
            | 42:45     | #7      | register     | rax           |                 |                |
            | 48:51     | #9      | reference    |               |                 | abc            |
            | --------- | ------- | ------------ | ------------- | --------------- | -------------- |
        """
    )
