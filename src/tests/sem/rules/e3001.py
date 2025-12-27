from i13c import ast, err, sem, src
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


def can_detect_immediate_out_of_range():
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
                        ref=src.Span(offset=12, length=20),
                        mnemonic=ast.Mnemonic(name=b"mov"),
                        operands=[
                            ast.Register(name=b"rax"),
                            ast.Immediate(value=0x1_FFFFFFFF_FFFFFFFF),
                        ],
                    )
                ],
            )
        ],
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3001.validate_immediate_out_of_range(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3001
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20
