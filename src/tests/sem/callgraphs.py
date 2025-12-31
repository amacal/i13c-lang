from i13c.sem import function, model, snippet, syntax
from tests.sem import prepare_program


def can_build_callgraphs_from_single_main():
    _, program = prepare_program(
        """
            fn main() { }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callgraph = semantic.callgraph

    assert len(callgraph) == 1
    target, callees = callgraph.popitem()

    assert isinstance(target, function.FunctionId)
    caller = semantic.basic.functions.get(target)

    assert caller.identifier.name == b"main"
    assert len(callees) == 0


def can_build_callgraphs_from_main_calling_snippet():
    _, program = prepare_program(
        """
            asm foo() noreturn { }
            fn main() noreturn { foo(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    callgraph = semantic.callgraph
    _, entrypoint = semantic.live.entrypoints.pop()

    assert len(callgraph) == 2
    assert isinstance(entrypoint.target, function.FunctionId)

    callees = callgraph[entrypoint.target]
    caller = semantic.basic.functions.get(entrypoint.target)

    assert caller.identifier.name == b"main"
    assert len(callees) == 1

    assert isinstance(callees[0][1], snippet.SnippetId)
    callee = semantic.basic.snippets.get(callees[0][1])

    assert callee.identifier.name == b"foo"
