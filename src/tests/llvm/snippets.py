from tests.llvm import prepare_graph


def can_lower_syscall_program():
    semantic, llvm = prepare_graph("""
        asm foo() noreturn { syscall; }
        fn main() noreturn { foo(); }
    """)

    assert llvm.flows.size() == 1

    function = semantic.find_function_by_name(b"main")
    assert function is not None

    instructions = llvm.instructions_of(function)
    assert list(instructions) == [
        ("SubRegImm", "4", "0"),
        ("SysCall",),
    ]


def can_lower_mov_program():
    semantic, llvm = prepare_graph("""
        asm foo() noreturn { mov rax, 0x1234; }
        fn main() noreturn { foo(); }
    """)

    assert llvm.flows.size() == 1

    function = semantic.find_function_by_name(b"main")
    assert function is not None

    instructions = llvm.instructions_of(function)
    assert list(instructions) == [
        ("SubRegImm", "4", "0"),
        ("MovRegImm", "0", "4660"),
    ]


def can_lower_mov_with_register_bound_slot():
    semantic, llvm = prepare_graph("""
        asm foo(dst@rax: u64, val@imm: u8) noreturn { mov dst, val; }
        fn main() noreturn { foo(0x01, 0x42); }
    """)

    assert llvm.flows.size() == 1

    function = semantic.find_function_by_name(b"main")
    assert function is not None

    instructions = llvm.instructions_of(function)
    assert list(instructions) == [
        ("SubRegImm", "4", "0"),
        ("MovRegImm", "0", "1"),
        ("MovRegImm", "0", "66"),
    ]


def can_lower_shl_program():
    semantic, llvm = prepare_graph("""
        asm foo() noreturn { shl rax, 0x41; }
        fn main() noreturn { foo(); }
    """)

    assert llvm.flows.size() == 1

    function = semantic.find_function_by_name(b"main")
    assert function is not None

    instructions = llvm.instructions_of(function)
    assert list(instructions) == [
        ("SubRegImm", "4", "0"),
        ("ShlRegImm", "0", "65"),
    ]


def can_lower_multiple_snippet_callsites():
    semantic, llvm = prepare_graph("""
        fn main() noreturn { foo(); bar(); }
        asm foo() { mov rax, 0x01; }
        asm bar() noreturn { syscall; }
    """)

    assert llvm.flows.size() == 1

    function = semantic.find_function_by_name(b"main")
    assert function is not None

    instructions = llvm.instructions_of(function)
    assert list(instructions) == [
        ("SubRegImm", "4", "0"),
        ("MovRegImm", "0", "1"),
        ("SysCall",),
    ]
