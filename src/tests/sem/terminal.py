from i13c.sem import model, syntax
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.indices.terminalities import Terminality
from tests.sem import prepare_program


def can_build_semantic_model_terminalities_empty():
    _, program = prepare_program(
        """
            fn main() { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 1
    id, terminality = terminalities.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(terminality, Terminality)

    assert terminality.noreturn is False


def can_build_semantic_model_terminalities_calls_terminal():
    _, program = prepare_program(
        """
            asm exit() noreturn { }
            fn main() { exit(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 1
    id, terminality = terminalities.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(terminality, Terminality)

    assert terminality.noreturn is True


def can_build_semantic_model_terminalities_calls_non_terminal():
    _, program = prepare_program(
        """
            asm exit() { }
            fn main() { exit(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 1
    id, terminality = terminalities.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(terminality, Terminality)

    assert terminality.noreturn is False


def can_build_semantic_model_terminalities_calls_without_accepted_resolutions():
    _, program = prepare_program(
        """
            fn main() { unknown(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    terminalities = semantic.indices.terminality_by_function

    assert terminalities.size() == 1
    id, terminality = terminalities.pop()

    assert isinstance(id, FunctionId)
    assert isinstance(terminality, Terminality)

    assert terminality.noreturn is False
