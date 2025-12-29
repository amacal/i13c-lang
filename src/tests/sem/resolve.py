from i13c.sem import callsite, function, model, resolve, snippet, syntax
from tests.sem import prepare_program


def can_build_semantic_model_accepted_resolutions_for_snippet():
    _, program = prepare_program(
        """
            asm foo(arg1@rax: u32) { }
            fn main() { foo(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.accepted) == 1
    assert len(value.rejected) == 0
    callables = value.accepted[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"


def can_build_semantic_model_rejected_resolutions_for_snippet_due_to_wrong_arity_much():
    _, program = prepare_program(
        """
            asm foo() { }
            fn main() { foo(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"wrong-arity"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"


def can_build_semantic_model_rejected_resolutions_for_snippet_due_to_wrong_arity_less():
    _, program = prepare_program(
        """
            asm foo(arg1@rax: u32) { }
            fn main() { foo(); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"wrong-arity"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"


def can_build_semantic_model_rejected_resolutions_for_snippet_due_to_wrong_hex_width():
    _, program = prepare_program(
        """
            asm foo(arg1@rax: u8) { }
            fn main() { foo(0x842); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"type-mismatch"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"


def can_resolve_function_and_snippet_with_same_name():
    _, program = prepare_program(
        """
            asm foo(arg1@rax: u32) { }
            fn foo() { }
            fn main() { foo(0x42); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    # we had two candidates by name
    assert len(value.accepted) == 1
    assert len(value.rejected) == 1

    # snippet was accepted
    accepted = value.accepted[0].callable
    assert accepted.kind == b"snippet"
    assert isinstance(accepted.target, snippet.SnippetId)

    snippet_value = semantic.snippets[accepted.target]
    assert snippet_value.identifier.name == b"foo"

    # function was rejected, due to wrong arity
    rejected = value.rejected[0].callable
    assert value.rejected[0].reason == b"wrong-arity"
    assert rejected.kind == b"function"
    assert isinstance(rejected.target, function.FunctionId)

    function_value = semantic.functions[rejected.target]
    assert function_value.identifier.name == b"foo"


def can_resolve_by_type_u64_max():
    _, program = prepare_program(
        """
            asm foo(arg1@rax: u64) { }
            fn main() { foo(0xffffffffffffffff); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.accepted) == 1
    assert len(value.rejected) == 0
    callables = value.accepted[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"


def can_reject_by_type_u64_overflow():
    _, program = prepare_program(
        """
            asm foo(arg1@rax: u64) { }
            fn main() { foo(0x10000000000000000); }
        """
    )

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.callsite_resolutions

    assert len(resolutions) == 1
    id, value = resolutions.popitem()

    assert isinstance(id, callsite.CallSiteId)
    assert isinstance(value, resolve.Resolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"type-mismatch"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, snippet.SnippetId)

    value = semantic.snippets[callables.target]
    assert value.identifier.name == b"foo"
