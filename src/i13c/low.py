from typing import List, Optional

from i13c import ast, diag, err, ir, res, src

# fmt: off
IR_REGISTER_MAP = {
    b"rax": 0, b"rcx": 1, b"rdx": 2, b"rbx": 3, b"rsp": 4, b"rbp": 5, b"rsi": 6, b"rdi": 7,
    b"r8": 8, b"r9": 9, b"r10": 10, b"r11": 11, b"r12": 12, b"r13": 13, b"r14": 14, b"r15": 15,
}
# fmt: on


class UnsupportedMnemonic(Exception):
    def __init__(self, ref: src.Span, name: bytes) -> None:
        self.ref = ref
        self.name = name


def lower(program: ast.Program) -> res.Result[ir.Unit, List[diag.Diagnostic]]:
    codeblocks: List[ir.CodeBlock] = []
    diagnostics: List[diag.Diagnostic] = []
    entry: Optional[int] = None

    try:
        for snippet in program.snippets:
            codeblocks.append(lower_snippet(snippet))

    except UnsupportedMnemonic as e:
        diagnostics.append(err.report_e4000_unsupported_mnemonic(e.ref, e.name))

    # check for duplicated symbols
    for idx, codeblock in enumerate(codeblocks):
        if codeblock.label:

            # find entry point
            if codeblock.label == b"main":
                entry = idx

    # any diagnostic is an error
    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(ir.Unit(entry=entry, codeblocks=codeblocks))


def lower_snippet(snippet: ast.Snippet) -> ir.CodeBlock:
    instructions: List[ir.Instruction] = []

    for instruction in snippet.instructions:
        instructions.append(lower_instruction(instruction))

    return ir.CodeBlock(
        label=snippet.name,
        noreturn=snippet.noreturn,
        instructions=instructions,
    )


def lower_instruction(instruction: ast.Instruction) -> ir.Instruction:
    if instruction.mnemonic.name == b"mov":
        return lower_instruction_mov(instruction)

    elif instruction.mnemonic.name == b"syscall":
        return lower_instruction_syscall(instruction)

    raise UnsupportedMnemonic(instruction.ref, instruction.mnemonic.name)


def lower_instruction_mov(instruction: ast.Instruction) -> ir.Instruction:
    dst = instruction.operands[0]
    src = instruction.operands[1]

    assert isinstance(dst, ast.Register)
    assert isinstance(src, ast.Immediate)

    dst_reg = IR_REGISTER_MAP[dst.name]
    src_imm = src.value

    return ir.MovRegImm(dst=dst_reg, imm=src_imm)


def lower_instruction_syscall(instruction: ast.Instruction) -> ir.Instruction:
    return ir.SysCall()
