from i13c import ast, err, sem, src
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


def can_detect_duplicated_slot_clobbers():
    program = ast.Program(
        functions=[],
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                noreturn=False,
                slots=[],
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
        ],
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3005.validate_duplicated_snippet_clobbers(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3005
    assert diagnostic.ref.offset == 1
    assert diagnostic.ref.length == 20
