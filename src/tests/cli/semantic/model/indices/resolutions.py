from i13c.cli.semantic.model import draw_list
from i13c.cli.semantic.model.indices.resolutions import (
    CallSiteResolutionListExtractor,
    InstructionResolutionListExtractor,
)
from i13c.sem.model import SemanticGraph
from tests.cli.semantic.model import prepare_semantic_graph


def can_draw_a_table_with_instruction_resolutions():
    graph: SemanticGraph = prepare_semantic_graph("""
        asm main() { mov rax, 0x01; }
    """)

    draw_list(InstructionResolutionListExtractor, graph).equals("""
        | --------- | -------------- | -------- | -------- | -------- | -------- |
        | Reference | Instruction ID | Mnemonic | Operands | Accepted | Rejected |
        | --------- | -------------- | -------- | -------- | -------- | -------- |
        | 22:36     | instruction#2  | mov      | 2        | 1        | 3        |
        | --------- | -------------- | -------- | -------- | -------- | -------- |
    """)


def can_draw_a_table_with_callsite_resolutions():
    graph: SemanticGraph = prepare_semantic_graph("""
        fn foo() {}
        fn foo(x: u16) {}
        fn main() { foo(0x123); }
    """)

    draw_list(CallSiteResolutionListExtractor, graph).equals("""
        | --------- | ----------- | ----------- | --------- | -------- | -------- |
        | Reference | CallSite ID | Callee Name | Arguments | Accepted | Rejected |
        | --------- | ----------- | ----------- | --------- | -------- | -------- |
        | 67:77     | callsite#5  | foo         | 1         | 1        | 1        |
        | --------- | ----------- | ----------- | --------- | -------- | -------- |
    """)
