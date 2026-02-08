from i13c.semantic import model, syntax
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import FunctionId
from i13c.semantic.typing.entities.snippets import SnippetId
from i13c.semantic.typing.resolutions.callsites import CallSiteResolution
from tests.sem import prepare_program


def can_resolve_callsite_calling_snippet():
    _, program = prepare_program("""
            asm foo(arg1@rax: u32) { }
            fn main() { foo(0x42); }
        """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.indices.resolution_by_callsite

    assert resolutions.size() == 1
    id, value = resolutions.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSiteResolution)

    assert len(value.accepted) == 1
    assert len(value.rejected) == 0
    callables = value.accepted[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, SnippetId)

    value = semantic.basic.snippets.get(callables.target)
    assert value.identifier.name == b"foo"


def can_resolve_callsite_calling_function():
    _, program = prepare_program("""
        fn foo(arg1: u32) { }
        fn main() { foo(0x42); }
    """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.indices.resolution_by_callsite

    assert resolutions.size() == 1
    id, value = resolutions.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSiteResolution)

    assert len(value.accepted) == 1
    assert len(value.rejected) == 0
    callables = value.accepted[0].callable

    assert callables.kind == b"function"
    assert isinstance(callables.target, FunctionId)

    value = semantic.basic.functions.get(callables.target)
    assert value.identifier.name == b"foo"


def can_reject_callsite_due_to_wrong_arity_more_than_expected():
    _, program = prepare_program("""
        asm foo() { }
        fn main() { foo(0x42); }
    """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.indices.resolution_by_callsite

    assert resolutions.size() == 1
    id, value = resolutions.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSiteResolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"wrong-arity"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, SnippetId)

    value = semantic.basic.snippets.get(callables.target)
    assert value.identifier.name == b"foo"


def can_reject_callsite_due_to_wrong_arity_less_than_expected():
    _, program = prepare_program("""
        asm foo(arg1@rax: u32) { }
        fn main() { foo(); }
    """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.indices.resolution_by_callsite

    assert resolutions.size() == 1
    id, value = resolutions.pop()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSiteResolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"wrong-arity"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, SnippetId)

    value = semantic.basic.snippets.get(callables.target)
    assert value.identifier.name == b"foo"


def can_reject_callsite_due_to_wrong_hex_width():
    _, program = prepare_program("""
        asm foo(arg1@rax: u8) { }
        fn main() { foo(0x842); }
    """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.indices.resolution_by_callsite

    assert resolutions.size() == 1
    id, value = resolutions.pop()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSiteResolution)

    assert len(value.rejected) == 1
    assert len(value.accepted) == 0

    assert value.rejected[0].reason == b"type-mismatch"
    callables = value.rejected[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, SnippetId)

    value = semantic.basic.snippets.get(callables.target)
    assert value.identifier.name == b"foo"


def can_resolve_function_and_snippet_with_same_name():
    _, program = prepare_program("""
        asm foo(arg1@rax: u32) { }
        fn foo() { }
        fn main() { foo(0x42); }
    """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.indices.resolution_by_callsite

    assert resolutions.size() == 1
    id, value = resolutions.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSiteResolution)

    # we had two candidates by name
    assert len(value.accepted) == 1
    assert len(value.rejected) == 1

    # snippet was accepted
    accepted = value.accepted[0].callable
    assert accepted.kind == b"snippet"
    assert isinstance(accepted.target, SnippetId)

    snippet_value = semantic.basic.snippets.get(accepted.target)
    assert snippet_value.identifier.name == b"foo"

    # function was rejected, due to wrong arity
    rejected = value.rejected[0].callable
    assert value.rejected[0].reason == b"wrong-arity"
    assert rejected.kind == b"function"
    assert isinstance(rejected.target, FunctionId)

    function_value = semantic.basic.functions.get(rejected.target)
    assert function_value.identifier.name == b"foo"


def can_resolve_by_type_u64_max():
    _, program = prepare_program("""
        asm foo(arg1@rax: u64) { }
        fn main() { foo(0xffffffffffffffff); }
    """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.indices.resolution_by_callsite

    assert resolutions.size() == 1
    id, value = resolutions.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSiteResolution)

    assert len(value.accepted) == 1
    assert len(value.rejected) == 0
    callables = value.accepted[0].callable

    assert callables.kind == b"snippet"
    assert isinstance(callables.target, SnippetId)

    value = semantic.basic.snippets.get(callables.target)
    assert value.identifier.name == b"foo"


def can_resolve_by_expression_as_arg():
    _, program = prepare_program("""
        fn foo(arg1: u64) { }
        fn main(arg2: u64) { foo(arg2); }
    """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.indices.resolution_by_callsite

    assert resolutions.size() == 1
    id, value = resolutions.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSiteResolution)

    assert len(value.accepted) == 1
    assert len(value.rejected) == 0

    callables = value.accepted[0].callable
    bindings = value.accepted[0].bindings

    assert callables.kind == b"function"
    assert isinstance(callables.target, FunctionId)

    value = semantic.basic.functions.get(callables.target)
    assert value.identifier.name == b"foo"

    assert len(bindings) == 1


def can_reject_by_expression_as_arg():
    _, program = prepare_program("""
        fn foo(arg1: u32) { }
        fn main(arg2: u64) { foo(arg2); }
    """)

    graph = syntax.build_syntax_graph(program)
    semantic = model.build_semantic_graph(graph)

    assert semantic is not None
    resolutions = semantic.indices.resolution_by_callsite

    assert resolutions.size() == 1
    id, value = resolutions.peak()

    assert isinstance(id, CallSiteId)
    assert isinstance(value, CallSiteResolution)

    assert len(value.accepted) == 0
    assert len(value.rejected) == 1

    callables = value.rejected[0].callable

    assert callables.kind == b"function"
    assert isinstance(callables.target, FunctionId)

    value = semantic.basic.functions.get(callables.target)
    assert value.identifier.name == b"foo"
