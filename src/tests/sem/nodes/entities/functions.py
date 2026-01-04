from i13c import ast
from i13c.sem import model, syntax
from i13c.sem.typing.entities.functions import Function, FunctionId
from tests.sem import prepare_program


def can_do_nothing_without_any_function():
    _, program = prepare_program(
        """
            asm main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    functions = semantic.basic.functions

    assert functions.size() == 0


def can_build_a_function_with_no_statements():
    _, program = prepare_program(
        """
            fn main() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    functions = semantic.basic.functions

    assert functions.size() == 1
    id, value = functions.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(value, Function)

    assert value.identifier.name == b"main"
    assert value.noreturn is True
    assert len(value.statements) == 0


def can_build_a_function_with_no_return_statement():
    _, program = prepare_program(
        """
            fn main() { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    functions = semantic.basic.functions

    assert functions.size() == 1
    id, value = functions.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(value, Function)

    assert value.identifier.name == b"main"
    assert value.noreturn is False
    assert len(value.statements) == 0


def can_build_a_function_with_call_statement():
    _, program = prepare_program(
        """
            fn main() { foo(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    functions = semantic.basic.functions

    assert functions.size() == 1
    id, value = functions.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(value, Function)

    assert value.identifier.name == b"main"
    assert value.noreturn is False

    assert len(value.statements) == 1
    sid = syntax.NodeId(value=value.statements[0].value)

    statement = graph.statements.get_by_id(sid)
    assert isinstance(statement, ast.CallStatement)

    assert statement.name == b"foo"
    assert len(statement.arguments) == 1
