from i13c import ast, err, sem, src
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


def can_detect_integer_literal_out_of_range():
    program = ast.Program(
        snippets=[],
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                noreturn=False,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=12, length=20),
                        name=b"foo",
                        arguments=[
                            ast.IntegerLiteral(
                                ref=src.Span(offset=34, length=18),
                                value=0x1FFFFFFFFFFFFFFFF,
                            )
                        ],
                    )
                ],
            )
        ],
    )

    model = build_semantic_graph(build_syntax_graph(program))
    diagnostics = sem.e3007.validate_integer_literal_out_of_range(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3007
    assert diagnostic.ref.offset == 34
    assert diagnostic.ref.length == 18
