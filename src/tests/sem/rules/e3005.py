from i13c import ast, err, sem, src
from i13c.sem.graph import build_graph


def can_detect_duplicated_asm_clobbers():
    program = ast.Program(
        functions=[
            ast.AsmFunction(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                terminal=False,
                parameters=[],
                clobbers=[
                    ast.Register(name=b"rax"),
                    ast.Register(name=b"rbx"),
                    ast.Register(name=b"rax"),
                ],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=22, length=6),
                        mnemonic=ast.Mnemonic(name=b"syscall"),
                        operands=[],
                    )
                ],
            )
        ]
    )

    graph = build_graph(program)
    diagnostics = sem.e3005.validate_duplicated_function_clobbers(graph)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3005
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20
