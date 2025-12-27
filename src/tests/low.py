from i13c import ast, err, ir, low, res, src
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


def can_lower_syscall_program():
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
                        ref=src.Span(offset=10, length=6),
                        mnemonic=ast.Mnemonic(name=b"syscall"),
                        operands=[],
                    ),
                ],
            )
        ],
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    unit = low.lower(model)
    assert isinstance(unit, res.Ok)
    assert unit.value.entry == 0

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1
    assert isinstance(instructions[0], ir.SysCall)


def can_lower_mov_program():
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
                        ref=src.Span(offset=10, length=10),
                        mnemonic=ast.Mnemonic(name=b"mov"),
                        operands=[
                            ast.Register(name=b"rax"),
                            ast.Immediate(value=0x1234),
                        ],
                    ),
                ],
            )
        ],
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    unit = low.lower(model)
    assert isinstance(unit, res.Ok)
    assert unit.value.entry == 0

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1

    instruction = instructions[0]
    assert isinstance(instruction, ir.MovRegImm)

    assert instruction.dst == 0
    assert instruction.imm == 0x1234


def can_lower_noentry_program():
    program = ast.Program(
        functions=[],
        snippets=[
            ast.Snippet(
                ref=src.Span(offset=0, length=4),
                name=b"aux",
                noreturn=False,
                slots=[],
                clobbers=[],
                instructions=[
                    ast.Instruction(
                        ref=src.Span(offset=10, length=6),
                        mnemonic=ast.Mnemonic(name=b"syscall"),
                        operands=[],
                    ),
                ],
            )
        ],
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    unit = low.lower(model)
    assert isinstance(unit, res.Ok)
    assert unit.value.entry is None

    codeblocks = unit.value.codeblocks
    assert len(codeblocks) == 1

    instructions = codeblocks[0].instructions
    assert len(instructions) == 1
    assert isinstance(instructions[0], ir.SysCall)


def can_detect_unsupported_mnemonic():
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
                        ref=src.Span(offset=10, length=4),
                        mnemonic=ast.Mnemonic(name=b"abcd"),
                        operands=[],
                    ),
                ],
            )
        ],
    )

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    unit = low.lower(model)
    assert isinstance(unit, res.Err)

    diagnostics = unit.error
    assert len(diagnostics) == 1

    assert diagnostics[0].code == err.ERROR_4000
    assert diagnostics[0].ref.offset == 10
    assert diagnostics[0].ref.length == 4
