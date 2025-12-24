from i13c import ast, err, sem, src
from i13c.sem.analysis import build_analysis
from i13c.sem.graph import build_graph


def can_detect_incorrect_argument_type_for_parameter():
    program = ast.Program(
        functions=[
            ast.RegFunction(
                ref=src.Span(offset=1, length=20),
                name=b"main",
                terminal=True,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=12, length=20),
                        name=b"foo",
                        arguments=[
                            ast.IntegerLiteral(
                                ref=src.Span(offset=15, length=4),
                                value=1042,
                            )
                        ],
                    )
                ],
            ),
            ast.RegFunction(
                ref=src.Span(offset=30, length=10),
                name=b"foo",
                terminal=True,
                parameters=[
                    ast.RegParameter(
                        name=b"x",
                        type=ast.Type(name=b"u8"),
                    )
                ],
                statements=[],
            ),
        ]
    )

    graph = build_graph(program)
    analysis = build_analysis(graph)
    diagnostics = sem.e3012.validate_called_arguments_types(graph, analysis)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3012
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 20
