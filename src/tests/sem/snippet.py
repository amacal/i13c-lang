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
    snippets = semantic.basic.snippets

    operands = semantic.basic.operands
    assert operands.size() == 2

    assert snippets.size() == 1
    id, value = snippets.pop()

    assert isinstance(id, snippet.SnippetId)
    assert isinstance(value, snippet.Snippet)

    assert value.identifier.name == b"main"
    assert value.noreturn is False

    assert len(value.instructions) == 1
    iid = value.instructions[0]

    assert isinstance(iid, asm.InstructionId)
    instruction = semantic.basic.instructions.get(iid)

    assert instruction.mnemonic.name == b"mov"
    assert len(instruction.operands) == 2

    operand0 = operands.get(instruction.operands[0])
    assert isinstance(operand0, asm.Operand)

    assert operand0.kind == b"register"
    assert isinstance(operand0.target, asm.Register)
    assert operand0.target.name == b"rax"

    operand1 = operands.get(instruction.operands[1])
    assert isinstance(operand1, asm.Operand)

    assert operand1.kind == b"immediate"
    assert isinstance(operand1.target, asm.Immediate)
    assert operand1.target.value == 0x1234
