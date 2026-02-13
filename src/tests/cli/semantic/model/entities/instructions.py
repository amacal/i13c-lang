from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.instructions import InstructionListExtractor
from tests.cli.semantic.model import prepare_artifacts


def can_draw_a_table_with_instructions():
    artifacts = prepare_artifacts("""
        asm main() { mov rax, rbx; }
    """)

    draw_list(InstructionListExtractor, artifacts).equals("""
        | --------- | -------------- | -------- | -------- |
        | Reference | Instruction ID | Mnemonic | Operands |
        | --------- | -------------- | -------- | -------- |
        | 22:35     | instruction#2  | mov      | 2        |
        | --------- | -------------- | -------- | -------- |
    """)
