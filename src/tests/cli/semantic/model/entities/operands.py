from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.entities.operands import OperandListExtractor
from i13c.sem.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_operands():
    graph: SemanticGraph = prepare_semantic_graph("""
        asm main(abc@rbx: u64) { mov rax, abc; }
    """)

    draw_list(OperandListExtractor, graph).equals("""
        | --------- | ---------- | ------------ | ------------- | -------------- | --------------- | --------------- | -------------- |
        | Reference | Operand ID | Operand Kind | Register Name | Register Width | Immediate Value | Immediate Width | Reference Name |
        | --------- | ---------- | ------------ | ------------- | -------------- | --------------- | --------------- | -------------- |
        | 38:41     | operand#3  | register     | rax           | 64             |                 |                 |                |
        | 43:46     | operand#4  | reference    |               |                |                 |                 | abc            |
        | --------- | ---------- | ------------ | ------------- | -------------- | --------------- | --------------- | -------------- |
    """)
