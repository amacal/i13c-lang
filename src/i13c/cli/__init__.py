import json
import os
import sys
from dataclasses import asdict

import click

from i13c import elf, enc, ld, lex, low, par, sem, src
from i13c.cli.core import BytesAsTextEncoder, emit_and_exit, unwrap
from i13c.cli.semantic import attach
from i13c.sem.model import build_semantic_graph
from i13c.sem.syntax import build_syntax_graph


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
        name = f"{lex.TOKEN_NAMES[token.code]:<15}"
        value = code.extract(token)

        click.echo(f"{key}:{name} -> {value!r}")


@i13c.command("ast")
@click.argument("path", type=click.Path(exists=True))
def ast_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    click.echo(json.dumps(asdict(program), cls=BytesAsTextEncoder))


@i13c.command("ir")
@click.argument("path", type=click.Path(exists=True))
def ir_command(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    code = src.open_text(text)
    tokens = unwrap(lex.tokenize(code), source=code)
    program = unwrap(par.parse(code, tokens), source=code)

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    if diagnostics := sem.validate(model, program):
        emit_and_exit(diagnostics, source=code)

    unit = unwrap(low.lower(model), source=code)

    for idx, codeblock in enumerate(unit.codeblocks):
        click.echo(f"Codeblock: {idx}")

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

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    if diagnostics := sem.validate(model, program):
        emit_and_exit(diagnostics, source=code)

    unit = unwrap(low.lower(model), source=code)
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

    graph = build_syntax_graph(program)
    model = build_semantic_graph(graph)

    if diagnostics := sem.validate(model, program):
        emit_and_exit(diagnostics, source=code)

    unit = unwrap(low.lower(model), source=code)
    linked = unwrap(ld.link(unit), source=code)
    binary = enc.encode(linked)
    executable = elf.emit(binary)

    with open("a.out", "wb") as f:
        f.write(executable)

    os.chmod("a.out", 0o755)


attach(i13c)
