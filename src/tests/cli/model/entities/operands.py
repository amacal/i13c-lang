from i13c.cli.model import draw_list
from i13c.cli.model.entities.operands import OperandListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_operands():
    artifacts = prepare_artifacts(
        """
            asm main(abc@rbx: u64) { mov rax, @abc; }
        """
    )

    draw_list(OperandListExtractor, artifacts).equals(
        """
            | --------- | ---------- | ------------ | ------------- | -------------- | --------------- | --------------- | -------------- |
            | Reference | Operand ID | Operand Kind | Register Name | Register Width | Immediate Value | Immediate Width | Reference Name |
            | --------- | ---------- | ------------ | ------------- | -------------- | --------------- | --------------- | -------------- |
            | 38:41     | operand#3  | register     | rax           | 64             |                 |                 |                |
            | 44:47     | operand#4  | reference    |               |                |                 |                 | abc            |
            | --------- | ---------- | ------------ | ------------- | -------------- | --------------- | --------------- | -------------- |
        """
    )
