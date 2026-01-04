from i13c.sem import model, syntax
from i13c.sem.typing.entities.functions import FunctionId
from i13c.sem.typing.entities.snippets import SnippetId
from tests.sem import prepare_program


def can_build_callgraphs_from_single_function():
    _, program = prepare_program(
        """
            fn main() { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callgraph = semantic.callgraph.calls_by_caller

    assert callgraph.size() == 1
    target, callees = callgraph.pop()

    assert isinstance(target, FunctionId)
    caller = semantic.basic.functions.get(target)

    assert caller.identifier.name == b"main"
    assert len(callees) == 0


def can_build_callgraphs_from_single_snippet():
    _, program = prepare_program(
        """
            asm foo() noreturn { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callgraph = semantic.callgraph.calls_by_caller

    assert callgraph.size() == 1
    target, callees = callgraph.pop()

    assert isinstance(target, SnippetId)
    caller = semantic.basic.snippets.get(target)

    assert caller.identifier.name == b"foo"
    assert len(callees) == 0


def can_build_callgraphs_when_function_calls_snippet():
    _, program = prepare_program(
        """
            asm foo() noreturn { }
            fn main() noreturn { foo(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callgraph = semantic.callgraph.calls_by_caller

    assert callgraph.size() == 2

    for cid, callees in callgraph.data.items():
        if isinstance(cid, SnippetId):
            assert len(callees) == 0
        else:
            assert len(callees) == 1
            assert isinstance(callees[0].target, SnippetId)
