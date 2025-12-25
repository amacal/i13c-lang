from i13c import ast, err, sem, src
from i13c.sem.graph import build_graph
from i13c.sem.model import build_model


def can_accept_operands_arity_of_syscall():
    program = ast.Program(
        functions=[],
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=0, length=4),
                name=b"main",
                noreturn=False,
                slots=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=0, length=7),
                        mnemonic=ast.Mnemonic(name=b"syscall"),
                        operands=[],
                    )
                ],
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 0


def can_accept_operands_arity_of_mov():
    program = ast.Program(
        functions=[],
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=0, length=4),
                name=b"main",
                noreturn=False,
                slots=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=0, length=3),
                        mnemonic=ast.Mnemonic(name=b"mov"),
                        operands=[
                            ast.Register(name=b"rax"),
                            ast.Immediate(value=0x1234),
                        ],
                    )
                ],
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 0


def can_detect_invalid_instruction():
    program = ast.Program(
        functions=[],
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=1, length=10),
                name=b"main",
                noreturn=False,
                slots=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=12, length=3),
                        mnemonic=ast.Mnemonic(name=b"xyz"),
                        operands=[],
                    )
                ],
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3000.validate_assembly_mnemonic(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3000
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 3
