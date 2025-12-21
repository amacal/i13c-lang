import os
import sys
import click

from typing import List
from i13c import ir, lex, par, src, sem, low, enc, elf, diag, res


def emit_and_exit(diagnostics: List[diag.Diagnostic]) -> None:
    for diagnostic in diagnostics:
        click.echo(
            f"Error {diagnostic.code} at offset {diagnostic.offset}: {diagnostic.message}"
        )

    sys.exit(1)


@click.group()
def i13c():
    pass


@i13c.command("tokenize")
@click.argument("path", type=click.Path(exists=True))
def tokenize_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = lex.tokenize(code)

    match tokens:
        case res.Err(diagnostics):
            return emit_and_exit(diagnostics)
        case res.Ok():
            pass

    for token in tokens.value:
        key = f"{token.code:03}:{token.offset:04}:{token.length:02}"
        value = code.extract(token)

        click.echo(f"{key} -> {value!r}")


@i13c.command("parse")
@click.argument("path", type=click.Path(exists=True))
def parse_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = lex.tokenize(code)

    match tokens:
        case res.Err(diagnostics):
            return emit_and_exit(diagnostics)
        case res.Ok():
            pass

    program = par.parse(code, tokens.value)

    for instruction in program.instructions:
        operands = ", ".join([str(op) for op in instruction.operands])
        click.echo(f"{str(instruction.mnemonic)} {operands}")


@i13c.command("lower")
@click.argument("path", type=click.Path(exists=True))
def lower_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = lex.tokenize(code)

    match tokens:
        case res.Err(diagnostics):
            return emit_and_exit(diagnostics)
        case res.Ok():
            pass

    program = par.parse(code, tokens.value)

    if diagnostics := sem.validate(program):
        emit_and_exit(diagnostics)

    if instructions := low.lower(program):
        for instr in instructions:
            click.echo(str(instr))


@i13c.command("encode")
@click.argument("path", type=click.Path(exists=True))
def encode_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = lex.tokenize(code)

    match tokens:
        case res.Err(diagnostics):
            return emit_and_exit(diagnostics)
        case res.Ok():
            pass

    program = par.parse(code, tokens.value)

    if diagnostics := sem.validate(program):
        emit_and_exit(diagnostics)

    instructions = low.lower(program)
    binary = enc.encode(instructions)

    sys.stdout.buffer.write(binary)


@i13c.command("compile")
@click.argument("path", type=click.Path(exists=True))
def compile_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = lex.tokenize(code)

    match tokens:
        case res.Err(diagnostics):
            return emit_and_exit(diagnostics)
        case res.Ok():
            pass

    program = par.parse(code, tokens.value)

    if diagnostics := sem.validate(program):
        emit_and_exit(diagnostics)

    instructions = low.lower(program)
    binary = enc.encode(instructions)

    executable = elf.emit(binary)

    with open("a.out", "wb") as f:
        f.write(executable)

    os.chmod("a.out", 0o755)
