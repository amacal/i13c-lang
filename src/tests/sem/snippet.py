from i13c.sem import asm, model, snippet, syntax
from tests.sem import prepare_program


def can_build_semantic_model_snippets():
    _, program = prepare_program(
        """
            asm main() { mov rax, 0x1234; }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    snippets = semantic.snippets

    assert len(snippets) == 1
    id, value = snippets.popitem()

    assert isinstance(id, snippet.SnippetId)
    assert isinstance(value, snippet.Snippet)

    assert value.identifier.name == b"main"
    assert value.noreturn is False

    assert len(value.instructions) == 1
    iid = value.instructions[0]

    assert isinstance(iid, asm.InstructionId)
    instruction = semantic.instructions[iid]

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    assert instruction.operands[0].kind == b"register"
    assert isinstance(instruction.operands[0].target, asm.Register)
    assert instruction.operands[0].target.name == b"rax"

    assert instruction.operands[1].kind == b"immediate"
    assert isinstance(instruction.operands[1].target, asm.Immediate)
    assert instruction.operands[1].target.value == 0x1234
