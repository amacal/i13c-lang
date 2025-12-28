from i13c import ir, ld, res


def can_move_entry_function_to_front():
    unit = ir.Unit(
        entry=1,
        codeblocks=[
            ir.CodeBlock(
                terminator=ir.Stop(),
                instructions=[
                    ir.MovRegImm(dst=1, imm=0x0),
                ],
            ),
            ir.CodeBlock(
                terminator=ir.FallThrough(target=0),
                instructions=[
                    ir.SysCall(),
                ],
            ),
        ],
    )

    linked = ld.link(unit)
    assert isinstance(linked, res.Ok)

    blocks = linked.value.codeblocks
    assert len(blocks) == 2

    # main should be first
    main_codeblock = blocks[0]
    assert len(main_codeblock.instructions) == 1
    assert isinstance(main_codeblock.instructions[0], ir.SysCall)

    # aux should be second
    aux_codeblock = blocks[1]
    assert len(aux_codeblock.instructions) == 1
    instruction = aux_codeblock.instructions[0]
    assert isinstance(instruction, ir.MovRegImm)
