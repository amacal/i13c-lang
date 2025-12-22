import os
import sys
import click

from typing import List, NoReturn
from i13c import lex, par, src, sem, low, enc, elf, diag, res


def emit_and_exit(diagnostics: List[diag.Diagnostic]) -> NoReturn:
    for diagnostic in diagnostics:
        click.echo(
            f"Error {diagnostic.code} at offset {diagnostic.offset}: {diagnostic.message}"
        )

    sys.exit(1)


def unwrap(result: res.Result[res.A, List[diag.Diagnostic]]) -> res.A:
    return res.unwrap(result, emit_and_exit)


@click.group()
def i13c():
    pass


@i13c.command("lex")
@click.argument("path", type=click.Path(exists=True))
def lex_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code))

    for token in tokens:
        key = f"{token.code:03}:{token.offset:04}:{token.length:02}"
        value = code.extract(token)

        click.echo(f"{key} -> {value!r}")


@i13c.command("ast")
@click.argument("path", type=click.Path(exists=True))
def ast_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code))
    program = unwrap(par.parse(code, tokens))

    for idx, function in enumerate(program.functions):
        click.echo(f"Function: {function.name.decode('utf-8')}")
        for instruction in function.instructions:
            operands = ", ".join([str(op) for op in instruction.operands])
            click.echo(f"  {str(instruction.mnemonic)} {operands}")

        if idx < len(program.functions) - 1:
            click.echo("")


@i13c.command("ir")
@click.argument("path", type=click.Path(exists=True))
def ir_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code))
    program = unwrap(par.parse(code, tokens))

    if diagnostics := sem.validate(program):
        emit_and_exit(diagnostics)

    if instructions := unwrap(low.lower(program)):
        for instr in instructions:
            click.echo(str(instr))


@i13c.command("bin")
@click.argument("path", type=click.Path(exists=True))
def bin_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code))
    program = unwrap(par.parse(code, tokens))

    if diagnostics := sem.validate(program):
        emit_and_exit(diagnostics)

    codeblocks = unwrap(low.lower(program))
    binary = enc.encode(codeblocks)

    sys.stdout.buffer.write(binary)


@i13c.command("elf")
@click.argument("path", type=click.Path(exists=True))
def elf_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code))
    program = unwrap(par.parse(code, tokens))

    if diagnostics := sem.validate(program):
        emit_and_exit(diagnostics)

    codeblocks = unwrap(low.lower(program))
    binary = enc.encode(codeblocks)
    executable = elf.emit(binary)

    with open("a.out", "wb") as f:
        f.write(executable)

    os.chmod("a.out", 0o755)
