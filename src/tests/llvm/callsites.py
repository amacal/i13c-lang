from tests.llvm import prepare_graph


def can_lower_function_calling_another_function():
    semantic, llvm = prepare_graph("""
        fn main() noreturn { foo(); }
        fn foo() noreturn { bar(); }
        asm bar() noreturn { syscall; }
    """)

    assert llvm.flows.size() == 2

    origin = semantic.find_function_by_name(b"main")
    assert origin is not None

    # TODO: check instructions
    # instructions = llvm.instructions_of(origin=origin)
    # assert list(instructions) == [
    #     ("SubRegImm", "4", "0"),
    #     ("SysCall",),
    # ]

    function = semantic.find_function_by_name(b"foo")
    assert function is not None

    block = llvm.find_block_by_origin(function)
    assert block is not None

    instructions = llvm.instructions_of(function)
    assert list(instructions) == [
        ("Label", str(block.value)),
        ("SubRegImm", "4", "0"),
        ("SysCall",),
    ]


def can_lower_function_calling_another_function_twice():
    semantic, llvm = prepare_graph("""
        fn main() noreturn { foo(); foo(); }
        fn foo() noreturn { bar(); }
        asm bar() noreturn { syscall; }
    """)

    assert llvm.flows.size() == 2

    origin = semantic.find_function_by_name(b"main")
    assert origin is not None

    # TODO: check instructions
    # instructions = llvm.instructions_of(origin=origin)
    # assert list(instructions) == [
    #     ("SubRegImm", "4", "0"),
    #     ("SysCall",),
    # ]

    function = semantic.find_function_by_name(b"foo")
    assert function is not None

    block = llvm.find_block_by_origin(function)
    assert block is not None

    instructions = llvm.instructions_of(function)
    assert list(instructions) == [
        ("Label", str(block.value)),
        ("SubRegImm", "4", "0"),
        ("SysCall",),
    ]
