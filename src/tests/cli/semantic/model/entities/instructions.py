from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.instructions import InstructionListExtractor
from i13c.sem.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_instructions():
    graph: SemanticGraph = prepare_semantic_graph("""
        asm main() { mov rax, rbx; }
    """)

    draw_list(InstructionListExtractor, graph).equals("""
        | --------- | -------------- | -------- | -------- |
        | Reference | Instruction ID | Mnemonic | Operands |
        | --------- | -------------- | -------- | -------- |
        | 22:35     | instruction#2  | mov      | 2        |
        | --------- | -------------- | -------- | -------- |
    """)
