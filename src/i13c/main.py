import os
import sys
from functools import partial
from typing import List, NoReturn

import click

from i13c import ast, diag, elf, enc, ld, lex, low, par, res, sem, src


def emit_and_exit(
    diagnostics: List[diag.Diagnostic], /, source: src.SourceCode
) -> NoReturn:
    for diagnostic in diagnostics:
        click.echo(
            f"Error {diagnostic.code} at offset {diagnostic.ref.offset}: {diagnostic.message}"
        )

    if diagnostics[0].ref.length > 0:
        click.echo("\n")
        click.echo(diag.show(source, diagnostics[0]))

    sys.exit(1)


def unwrap(
    result: res.Result[res.A, List[diag.Diagnostic]], /, source: src.SourceCode
) -> res.A:
    return res.unwrap(result, partial(emit_and_exit, source=source))


@click.group()
def i13c():
    pass


@i13c.command("lex")
@click.argument("path", type=click.Path(exists=True))
def lex_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)

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
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    for idx, function in enumerate(program.functions):
        click.echo(f"Function: {function.name.decode('utf-8')}")

        if function.parameters:
            click.echo("  Parameters:")
            for parameter in function.parameters:
                click.echo(f"    {str(parameter)}")

        if isinstance(function, ast.AsmFunction) and function.instructions:
            click.echo("  Instructions:")
            for instruction in function.instructions:
                click.echo(f"    {str(instruction)}")

        if isinstance(function, ast.RegFunction) and function.statements:
            click.echo("  Statements:")
            for statement in function.statements:
                click.echo(f"    {str(statement)}")

        if idx < len(program.functions) - 1:
            click.echo("")


@i13c.command("ir")
@click.argument("path", type=click.Path(exists=True))
def ir_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    if diagnostics := sem.validate_1st_pass(program):
        emit_and_exit(diagnostics, source=code)

    unit = unwrap(low.lower(program), source=code)

    for idx, codeblock in enumerate(unit.codeblocks):
        click.echo(
            f"Codeblock: {codeblock.label.decode('utf-8') if codeblock.label else '<anonymous>'}"
        )
        for instruction in codeblock.instructions:
            click.echo(f"  {str(instruction)}")

        if idx < len(unit.codeblocks) - 1:
            click.echo("")


@i13c.command("bin")
@click.argument("path", type=click.Path(exists=True))
def bin_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    if diagnostics := sem.validate_1st_pass(program):
        emit_and_exit(diagnostics, source=code)

    unit = unwrap(low.lower(program), source=code)
    linked = unwrap(ld.link(unit), source=code)
    binary = enc.encode(linked)

    sys.stdout.buffer.write(binary)


@i13c.command("elf")
@click.argument("path", type=click.Path(exists=True))
def elf_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    if diagnostics := sem.validate_1st_pass(program):
        emit_and_exit(diagnostics, source=code)

    unit = unwrap(low.lower(program), source=code)
    linked = unwrap(ld.link(unit), source=code)
    binary = enc.encode(linked)
    executable = elf.emit(binary)

    with open("a.out", "wb") as f:
        f.write(executable)

    os.chmod("a.out", 0o755)
