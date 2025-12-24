from i13c import ast, err, sem, src
from i13c.sem.analysis import build_analysis
from i13c.sem.graph import build_graph


def can_detect_non_asm_called_symbol():
    program = ast.Program(
        functions=[
            ast.RegFunction(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                terminal=False,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=12, length=20),
                        name=b"foo",
                        arguments=[],
                    )
                ],
            ),
            ast.RegFunction(
                ref=src.Span(offset=30, length=10),
                name=b"foo",
                terminal=True,
                parameters=[],
                statements=[],
            ),
        ]
    )

    graph = build_graph(program)
    analysis = build_analysis(graph)
    diagnostics = sem.e3009.validate_called_symbol_is_asm(graph, analysis)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3009
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20
