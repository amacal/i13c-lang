from i13c.cli.model import draw_list
from i13c.cli.model.resolutions.instructions import InstructionResolutionListExtractor
from tests.cli.model import prepare_artifacts


def can_draw_a_table_with_instruction_resolutions():
    artifacts = prepare_artifacts(
        """
            asm main() { mov rax, 0x01; }
        """
    )

    draw_list(InstructionResolutionListExtractor, artifacts).equals(
        """
            | --------- | -------------- | -------- | -------- | -------- | -------- |
            | Reference | Instruction ID | Mnemonic | Operands | Accepted | Rejected |
            | --------- | -------------- | -------- | -------- | -------- | -------- |
            | 26:40     | instruction#2  | mov      | 2        | 1        | 4        |
            | --------- | -------------- | -------- | -------- | -------- | -------- |
        """
    )
