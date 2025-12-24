from i13c import ast, err, sem, src
from i13c.sem.graph import build_graph


def can_detect_invalid_asm_operand_types_of_mov():
    program = ast.Program(
        functions=[
            ast.AsmFunction(
                ref=src.Span(offset=1, length=10),
                name=b"main",
                terminal=False,
                parameters=[],
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
        ]
    )

    graph = build_graph(program)
    diagnostics = sem.e3002.validate_assembly_operand_types(graph)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3002
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 15
