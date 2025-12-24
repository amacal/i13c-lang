from i13c import ast, err, sem, src
from i13c.sem import build


def can_accept_asm_operands_arity_of_syscall():
    program = ast.Program(
        functions=[
            ast.AsmFunction(
                ref=src.Span(offset=0, length=4),
                name=b"main",
                terminal=False,
                parameters=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=0, length=7),
                        mnemonic=ast.Mnemonic(name=b"syscall"),
                        operands=[],
                    )
                ],
            )
        ]
    )

    relationships = build.build_semantic(program)
    diagnostics = sem.e3000.validate_assembly_mnemonic(relationships)

    assert len(diagnostics) == 0


def can_accept_asm_operands_arity_of_mov():
    program = ast.Program(
        functions=[
            ast.AsmFunction(
                ref=src.Span(offset=0, length=4),
                name=b"main",
                terminal=False,
                parameters=[],
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
        ]
    )

    relationships = build.build_semantic(program)
    diagnostics = sem.e3000.validate_assembly_mnemonic(relationships)

    assert len(diagnostics) == 0


def can_detect_invalid_asm_instruction():
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
                        ref=src.Span(offset=12, length=3),
                        mnemonic=ast.Mnemonic(name=b"xyz"),
                        operands=[],
                    )
                ],
            )
        ]
    )

    relationships = build.build_semantic(program)
    diagnostics = sem.e3000.validate_assembly_mnemonic(relationships)

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]

    assert diagnostic.code == err.ERROR_3000
    assert diagnostic.ref.offset == 12
    assert diagnostic.ref.length == 3
