from i13c import ir, ld, res


def can_move_entry_function_to_front():
    codeblocks = [
        ir.CodeBlock(
            label=b"aux",
            instructions=[
                ir.MovRegImm(dst=1, imm=0x0),
            ],
        ),
        ir.CodeBlock(
            label=b"main",
            instructions=[
                ir.SysCall(),
            ],
        ),
    ]

    linked = ld.link(codeblocks)
    assert isinstance(linked, res.Ok)
    assert len(linked.value) == 2

    # main should be first
    main_codeblock = linked.value[0]
    assert len(main_codeblock.instructions) == 1
    assert isinstance(main_codeblock.instructions[0], ir.SysCall)

    # aux should be second
    aux_codeblock = linked.value[1]
    assert len(aux_codeblock.instructions) == 1
    instruction = aux_codeblock.instructions[0]
    assert isinstance(instruction, ir.MovRegImm)
