from typing import List

from tests.llvm import prepare_graph


class MissingMainInFixture(Exception):
    def __init__(self) -> None:
        super().__init__("main function is missing in fixture")


def prepare_snippet(code: str) -> List[str]:
    semantic, llvm = prepare_graph(code)

    # if main is found return all instructions in main
    if main := semantic.find_function_by_name(b"main"):
        return list(llvm.instructions_of(main))

    raise MissingMainInFixture()


def can_lower_multiple_callsites():
    instructions = prepare_snippet("""
        fn main() noreturn { foo(); bar(); }
        asm foo() { mov rax, 0x01; }
        asm bar() noreturn { syscall; }
    """)

    assert instructions == [
        "mov rax, 0x00000001",
        "syscall",
    ]
