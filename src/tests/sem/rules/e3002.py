from i13c import ast, err, sem, src
from i13c.sem.graph import build_graph
from i13c.sem.model import build_model


def can_detect_invalid_operand_types_of_mov():
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
                        ref=src.Span(offset=12, length=15),
                        mnemonic=ast.Mnemonic(name=b"mov"),
                        operands=[
                            ast.Immediate(value=0x1234),
                            ast.Immediate(value=0x5678),
                        ],
                    )
                ],
            )
        ],
    )

    model = build_model(build_graph(program))
    diagnostics = sem.e3002.validate_assembly_operand_types(model)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3002
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 15
