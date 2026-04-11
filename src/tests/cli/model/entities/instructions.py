from i13c.cli.model import draw_list
from i13c.cli.model.entities.instructions import InstructionListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_instructions():
    artifacts = prepare_artifacts(
        """
            asm main() { mov rax, rbx; }
        """
    )

    draw_list(InstructionListExtractor, artifacts).equals(
        """
            | --------- | -------------- | -------- | -------- |
            | Reference | Instruction ID | Mnemonic | Operands |
            | --------- | -------------- | -------- | -------- |
            | 26:39     | instruction#3  | mov      | 2        |
            | --------- | -------------- | -------- | -------- |
        """
    )
