from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.snippets import SnippetId
from tests.sem import prepare_program


def can_build_callgraphs_from_single_function():
    _, program = prepare_program("""
        fn main() { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    callgraph = semantic.callgraph.calls_by_callee

    assert callgraph.size() == 1
    target, callers = callgraph.peak()

    assert isinstance(target, FunctionId)
    caller = semantic.basic.functions.get(target)

    assert caller.identifier.name == b"main"
    assert len(callers) == 0


def can_build_callgraphs_from_single_snippet():
    _, program = prepare_program("""
        asm foo() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    callgraph = semantic.callgraph.calls_by_callee

    assert callgraph.size() == 1
    target, callers = callgraph.peak()

    assert isinstance(target, SnippetId)
    caller = semantic.basic.snippets.get(target)

    assert caller.identifier.name == b"foo"
    assert len(callers) == 0


def can_build_callgraphs_when_function_calls_snippet():
    _, program = prepare_program("""
        asm foo() noreturn { }
        fn main() noreturn { foo(); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    callgraph = semantic.callgraph.calls_by_callee

    assert callgraph.size() == 2

    for cid, callers in callgraph.data.items():
        if isinstance(cid, FunctionId):
            assert len(callers) == 0
        else:
            assert len(callers) == 1
            assert isinstance(callers[0].target, FunctionId)
