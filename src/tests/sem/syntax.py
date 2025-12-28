from i13c import ast, src
from i13c.sem.syntax import NodesVisitor


def can_visit_all_nodes_in_a_snippet() -> None:
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

    visitor = NodesVisitor()
    program.accept(visitor)

    assert len(list(visitor.nodes.snippets.items())) == 1
    assert len(list(visitor.nodes.instructions.items())) == 1

    assert len(list(visitor.nodes.functions.items())) == 0
    assert len(list(visitor.nodes.statements.items())) == 0
    assert len(list(visitor.nodes.literals.items())) == 0


def can_visit_all_nodes_in_a_function() -> None:
    program = ast.Program(
        functions=[
            ast.Function(
                ref=src.Span(offset=1, length=10),
                name=b"main",
                noreturn=False,
                parameters=[],
                statements=[
                    ast.CallStatement(
                        ref=src.Span(offset=11, length=20),
                        name=b"foo",
                        arguments=[
                            ast.IntegerLiteral(
                                ref=src.Span(offset=21, length=30),
                                value=42,
                            ),
                        ],
                    )
                ],
            )
        ],
        snippets=[],
    )

    visitor = NodesVisitor()
    program.accept(visitor)

    assert len(list(visitor.nodes.functions.items())) == 1
    assert len(list(visitor.nodes.statements.items())) == 1
    assert len(list(visitor.nodes.literals.items())) == 1

    assert len(list(visitor.nodes.snippets.items())) == 0
    assert len(list(visitor.nodes.instructions.items())) == 0
