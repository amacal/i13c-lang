from i13c import ast, err, sem, src
from i13c.sem.graph import build_graph
from i13c.sem.model import build_model


def can_detect_duplicated_slot_names():
    program = ast.Program(
        functions=[],
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                noreturn=False,
                slots=[
                    ast.Slot(
                        name=b"code",
                        type=ast.Type(name=b"u32"),
                        bind=ast.Register(name=b"rdi"),
                    ),
                    ast.Slot(
                        name=b"code",
                        type=ast.Type(name=b"u16"),
                        bind=ast.Register(name=b"rax"),
                    ),
                ],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=22, length=6),
                        mnemonic=ast.Mnemonic(name=b"syscall"),
                        operands=[],
                    )
                ],
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3004.validate_duplicated_parameter_names(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3004
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20


def can_detect_duplicated_parameter_names():
    program = ast.Program(
        snippets=[],
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                noreturn=False,
                parameters=[
                    ast.Parameter(
                        name=b"code",
                        type=ast.Type(name=b"u32"),
                    ),
                    ast.Parameter(
                        name=b"code",
                        type=ast.Type(name=b"u16"),
                    ),
                ],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=22, length=6),
                        name=b"foo",
                        arguments=[],
                    )
                ],
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3004.validate_duplicated_parameter_names(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3004
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20
