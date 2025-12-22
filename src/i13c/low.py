from typing import List, Set

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


def lower(program: ast.Program) -> res.Result[ir.Unit, List[diag.Diagnostic]]:
    codeblocks: List[ir.CodeBlock] = []
    diagnostics: List[diag.Diagnostic] = []
    symbols: Set[bytes] = set()

    try:
        for function in program.functions:
            codeblocks.append(lower_function(function))

    except UnknownMnemonic as ex:
        diagnostics.append(report_unknown_instruction(ex.ref, ex.name))

    # check for duplicated symbols
    for codeblock in codeblocks:
        if codeblock.label not in symbols:
            symbols.add(codeblock.label)
        else:
            diagnostics.append(report_duplicate_symbol(codeblock.label))

    # any diagnostic is an error
    if diagnostics:
        return res.Err(diagnostics)

    return res.Ok(ir.Unit(symbols=symbols, codeblocks=codeblocks))


def lower_function(function: ast.Function) -> ir.CodeBlock:
    instructions: List[ir.Instruction] = []

    for instruction in function.instructions:
        instructions.append(lower_instruction(instruction))

    return ir.CodeBlock(label=function.name, instructions=instructions)


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


def report_duplicate_symbol(name: bytes) -> diag.Diagnostic:
    return diag.Diagnostic(
        code="V002",
        offset=0,
        message=f"Duplicate symbol definition: {name.decode()}",
    )
