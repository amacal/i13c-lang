from typing import List, Optional

from i13c import ast, diag, ir, res

# fmt: off
IR_REGISTER_MAP = {
    b"rax": 0, b"rcx": 1, b"rdx": 2, b"rbx": 3, b"rsp": 4, b"rbp": 5, b"rsi": 6, b"rdi": 7,
    b"r8": 8, b"r9": 9, b"r10": 10, b"r11": 11, b"r12": 12, b"r13": 13, b"r14": 14, b"r15": 15,
}
# fmt: on


class UnknownMnemonic(Exception):
    def __init__(self, ref: ast.Reference, name: bytes) -> None:
        self.ref = ref
        self.name = name


def lower(
    program: ast.Program,
) -> res.Result[List[ir.CodeBlock], List[diag.Diagnostic]]:
    entry: Optional[int] = None
    codeblocks: List[ir.CodeBlock] = []
    diagnostics: List[diag.Diagnostic] = []

    try:
        for function in program.functions:
            if function.name == b"main":
                entry = len(codeblocks)

            codeblocks.append(lower_function(function))

    except UnknownMnemonic as ex:
        diagnostics.append(report_unknown_instruction(ex.ref, ex.name))

    if entry is None:
        diagnostics.append(report_missing_main_function())

    # any diagnostic is an error
    if diagnostics:
        return res.Err(diagnostics)

    # linting cannot infer it
    assert entry is not None

    # move entrypoint to the front
    codeblocks = [codeblocks[entry]] + [
        codeblock for idx, codeblock in enumerate(codeblocks) if idx != entry
    ]

    return res.Ok(codeblocks)


def lower_function(function: ast.Function) -> ir.CodeBlock:
    instructions: List[ir.Instruction] = []

    for instruction in function.instructions:
        instructions.append(lower_instruction(instruction))

    return ir.CodeBlock(instructions=instructions)


def lower_instruction(instruction: ast.Instruction) -> ir.Instruction:
    if instruction.mnemonic.name == b"mov":
        return lower_instruction_mov(instruction)

    elif instruction.mnemonic.name == b"syscall":
        return lower_instruction_syscall(instruction)

    raise UnknownMnemonic(instruction.ref, instruction.mnemonic.name)


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


def report_unknown_instruction(ref: ast.Reference, name: bytes) -> diag.Diagnostic:
    return diag.Diagnostic(
        code="V001",
        offset=ref.offset,
        message=f"Unknown instruction mnemonic: {name.decode()}",
    )


def report_missing_main_function() -> diag.Diagnostic:
    return diag.Diagnostic(
        code="V002",
        offset=0,
        message="Missing 'main' entrypoint function",
    )
