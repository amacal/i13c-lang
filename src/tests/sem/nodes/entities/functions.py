from i13c.graph.nodes import run as run_graph
from i13c.semantic.typing.entities.callsites import CallSiteId
from i13c.semantic.typing.entities.functions import Function, FunctionId
from tests.sem import prepare_program


def can_do_nothing_without_any_function():
    _, program = prepare_program("""
        asm main() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    functions = semantic.basic.functions

    assert functions.size() == 0


def can_build_a_function_with_no_statements():
    _, program = prepare_program("""
        fn main() noreturn { }
    """)

    semantic = run_graph(program).semantic_graph()

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
    _, program = prepare_program("""
        fn main() { }
    """)

    semantic = run_graph(program).semantic_graph()

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
    _, program = prepare_program("""
        fn main() { foo(0x42); }
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    functions = semantic.basic.functions

    assert functions.size() == 1
    id, value = functions.peak()

    assert isinstance(id, FunctionId)
    assert isinstance(value, Function)

    assert value.identifier.name == b"main"
    assert value.noreturn is False

    assert len(value.statements) == 1
    assert isinstance(value.statements[0], CallSiteId)

    callsite = semantic.basic.callsites.get(value.statements[0])

    assert callsite.callee.name == b"foo"
    assert len(callsite.arguments) == 1


def can_build_function_with_properly_derived_types():
    _, program = prepare_program("""
        fn main(
            r1: u64[0x0000..0xffff],
            r2: u8[0x00..0x10]
        ) {}
    """)

    semantic = run_graph(program).semantic_graph()

    assert semantic is not None
    functions = semantic.basic.functions
    parameters = semantic.basic.parameters

    assert functions.size() == 1
    _, value = functions.peak()

    assert value.identifier.name == b"main"
    assert len(value.parameters) == 2

    param1 = parameters.get(value.parameters[0])
    assert param1.ident.name == b"r1"
    assert param1.type.name == b"u64"
    assert param1.type.width == 16
    assert param1.type.range.lower == 0x0000
    assert param1.type.range.upper == 0xFFFF

    param2 = parameters.get(value.parameters[1])
    assert param2.ident.name == b"r2"
    assert param2.type.name == b"u8"
    assert param2.type.width == 8
    assert param2.type.range.lower == 0x00
    assert param2.type.range.upper == 0x10
